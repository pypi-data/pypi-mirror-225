from __future__ import annotations

import asyncio
import re
import sqlite3
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Final, Sequence, cast

import aiosqlite
import orjson
from pydantic import BaseModel

from beni import block, bpath
from beni.bfunc import getSqlPlacement, toAny
from beni.btype import Null, XPath

sqlite3.register_converter(
    "bool",
    lambda x: x not in (
        b'',
        b'0',
        # None, # 如果是None根本就不会进来，这里判断也没有意义
    )
)

_ALIVE: Final = 5 * 60  # 数据库链接至少存活时间（因为清除不是实时执行）


class SqliteDbPool:

    _isRunningClean = False

    def __init__(self, dbFile: XPath, maxConnections: int = 10):
        self._avaliableList: asyncio.Queue[_SqliteDbWrite] = asyncio.Queue()
        self.lock = block.RWLock(maxConnections)
        if type(dbFile) is Path:
            self._dbFile = dbFile
        else:
            self._dbFile = bpath.get(dbFile)

    def exists(self):
        return self._dbFile.exists()

    async def _clean(self):
        while True:
            await asyncio.sleep(_ALIVE)
            now = time.monotonic()
            dbList: list[_SqliteDbWrite] = []
            while not self._avaliableList.empty():
                db = self._avaliableList.get_nowait()
                if now - db._releaseTime > _ALIVE:  # type: ignore
                    await db.close()
                else:
                    dbList.append(db)
            for db in dbList:
                self._avaliableList.put_nowait(db)

    async def close(self, isWriteLock: bool = True):
        if isWriteLock:
            await self.lock.getWrite()
        while not self._avaliableList.empty():
            db = self._avaliableList.get_nowait()
            await db.close()
        if isWriteLock:
            self.lock.releaseWrite()

    async def _getDb(self):
        if self._avaliableList.empty():
            db = _SqliteDbWrite()
            await db.connect(self._dbFile)
            #
            if not self._isRunningClean:
                self._isRunningClean = True
                asyncio.create_task(self._clean())
        else:
            db = self._avaliableList.get_nowait()
        return db

    def _releaseDb(self, db: _SqliteDbWrite):
        db._releaseTime = time.monotonic()  # type: ignore 访问私有变量
        self._avaliableList.put_nowait(db)

    @asynccontextmanager
    async def _useDb(self):
        db = await self._getDb()
        try:
            yield db
        finally:
            self._releaseDb(db)

    @asynccontextmanager
    async def read(self):
        async with self.lock.useRead():
            async with self._useDb() as db:
                yield cast(_SqliteDbRead, db)

    @asynccontextmanager
    async def write(self):
        async with self.lock.useWrite():
            async with self._useDb() as db:
                try:
                    yield db
                    await db.commit()
                except:
                    await db.rollback()
                    raise

    async def add(self, table: str, data: dict[str, Any]):
        async with self.write() as db:
            return await db.add(table, data)

    async def addList(self, table: str, dataList: list[dict[str, Any]]):
        async with self.write() as db:
            return await db.addList(table, dataList)

    async def update(self, table: str, data: dict[str, Any], statement: str = '', *whereValues: Any):
        async with self.write() as db:
            return await db.update(table, data, statement, *whereValues)

    async def get(self, sql: str, *parameters: Any):
        async with self.read() as db:
            return await db.get(sql, *parameters)

    async def getList(self, sql: str, *parameters: Any):
        async with self.read() as db:
            return await db.getList(sql, *parameters)

    async def value(self, sql: str, *parameters: Any):
        async with self.read() as db:
            return await db.value(sql, *parameters)

    async def execute(self, sql: str, *parameters: Any):
        async with self.write() as db:
            return await db.execute(sql, *parameters)


class _SqliteDbRead:

    _db: aiosqlite.Connection
    _releaseTime = 0.0

    async def connect(self, db_file: XPath):
        self._db = await aiosqlite.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        self._db.row_factory = sqlite3.Row

    async def close(self):
        await self._db.close()

    async def get(self, sql: str, *parameters: Any):
        async with self._db.execute(sql, parameters) as cursor:
            return await cursor.fetchone()

    async def getList(self, sql: str, *parameters: Any):
        async with self._db.execute(sql, parameters) as cursor:
            return cast(list[sqlite3.Row], await cursor.fetchall())

    async def value(self, sql: str, *parameters: Any):
        row = await self.get(sql, *parameters)
        assert row
        return row[0]


class _SqliteDbWrite(_SqliteDbRead):

    async def add(self, table: str, data: dict[str, Any]):
        keylist = sorted(data.keys())
        fieldname_list = ','.join([f'"{x}"' for x in keylist])
        fieldvalue_list = [data[x] for x in keylist]
        async with self._db.execute(
            f'''
            INSERT INTO `{table}` ({fieldname_list})
            VALUES
                {getSqlPlacement(keylist)}
            ''',
            fieldvalue_list,
        ) as cursor:
            return cursor.lastrowid

    async def addList(self, table: str, dataList: list[dict[str, Any]]):
        keyset: set[str] = set()
        for data in dataList:
            keyset.update(data.keys())
        keylist = sorted(keyset)
        fieldname_list = ','.join([f'`{x}`' for x in keylist])
        fieldvalue_list = [[data.get(key) for key in keylist] for data in dataList]
        async with self._db.executemany(
            f'''
            INSERT INTO `{table}` ({fieldname_list})
            VALUES
                {getSqlPlacement(keylist)}
            ''',
            fieldvalue_list
        ) as cursor:
            return cursor.rowcount

    async def update(self, table: str, data: dict[str, Any], statement: str = '', *whereValues: Any):
        keylist = sorted(data.keys())
        fieldname_list = ','.join([f'`{x}`=?' for x in keylist])
        fieldvalue_list = [data[x] for x in keylist] + list(whereValues)
        async with self._db.execute(
            f'''
            UPDATE `{table}`
            SET {fieldname_list}
            {statement}
            ''',
            fieldvalue_list,
        ) as cursor:
            return cursor.rowcount

    async def execute(self, sql: str, *parameters: Any):
        async with self._db.execute(sql, parameters) as cursor:
            return cursor.rowcount

    async def commit(self):
        return await self._db.commit()

    async def rollback(self):
        return await self._db.rollback()


_RE_TABLE_NAME: Final = re.compile(r'(.*?)Model$')


class SqliteDbModel(BaseModel):

    __tableName__ = ''

    _db: SqliteDbPool = cast(SqliteDbPool, None)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps

    @classmethod
    def setDb(cls, data: SqliteDbPool):
        cls._db = data

    @classmethod
    def getDb(cls):
        return cls._db

    @classmethod
    @property
    def TableName(cls):
        if not cls.__tableName__:
            name: str = _RE_TABLE_NAME.findall(cls.__name__)[0]
            nameList = list(name)
            nameList[0] = nameList[0].lower()
            for i in range(len(nameList)):
                v = nameList[i]
                if v.isupper():
                    nameList[i] = f'_{v.lower()}'
            result = ''.join(nameList)
            cls.__tableName__ = result
        return cls.__tableName__

    async def add(self):
        return await self._add()

    async def _add(self, exclude: set[str] = Null, include: set[str] = Null):
        return await self._db.add(
            self.TableName,
            self.dict(
                exclude=toAny(exclude),
                include=toAny(include),
            )
        )

    @classmethod
    async def addList(cls, modelList: Sequence[SqliteDbModel]):
        return await cls._addList(modelList)

    @classmethod
    async def _addList(cls, modelList: Sequence[SqliteDbModel], exclude: set[str] = Null):
        if not modelList:
            return 0
        return await cls._db.addList(
            cls.TableName,
            [x.dict(exclude=toAny(exclude)) for x in modelList],
        )

    async def _update(self, statement: str = '', *args: Any, exclude: set[str] = Null, include: set[str] = Null):
        return await self._db.update(
            self.TableName,
            self.dict(
                exclude=toAny(exclude),
                include=toAny(include),
            ),
            statement,
            *args,
        )

    @classmethod
    async def removeAll(cls):
        return await cls._remove()

    @classmethod
    async def _remove(cls, statement: str = '', *args: Any):
        return await cls._db.execute(
            f'DELETE FROM {cls.TableName} {statement}',
            *args,
        )

    @classmethod
    async def _get(cls, statement: str = '', *args: Any, fields: set[str] = Null):
        row = await cls._db.get(
            f'''
            SELECT                
                {', '.join(fields) if fields else '*'}
            FROM
                `{cls.TableName}`
            {statement}
            LIMIT 1
            ''',
            *args,
        )
        if row:
            return cls(**dict(row))

    @classmethod
    async def _getList(cls, statement: str = '', *args: Any, fields: set[str] = Null):
        rowList = await cls._db.getList(
            f'''
            SELECT
                {', '.join(fields) if fields else '*'}
            FROM
                `{cls.TableName}`
            {statement}
            ''',
            *args,
        )
        return [cls(**dict(x)) for x in rowList]

    @classmethod
    async def _count(cls, statement: str = '', *args: Any) -> int:
        return await cls._db.value(
            f'''
            SELECT
                COUNT( * )
            FROM
                `{cls.TableName}`
            {statement}
            ''',
            *args,
        )
