import os
import shutil
import sys
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from beni.bfunc import runThread
from beni.btype import XPath


def get(path: XPath, expand: str = ''):
    if type(path) is not Path:
        path = Path(path)
    return path.joinpath(expand).resolve()


def user(expand: str = ''):
    return get(Path('~').expanduser(), expand)


def desktop(expand: str = ''):
    return user(f'Desktop/{expand}')


def workspace(expand: str = ''):
    if sys.platform == 'win32':
        return get(f'C:/beni-workspace/{expand}')
    else:
        return get(f'/data/beni-workspace/{expand}')


def tempFile():
    return workspace(f'temp/{uuid.uuid4()}.tmp')


def tempPath():
    return workspace(f'temp/{uuid.uuid4()}')


def changeRelative(target: XPath, fromRelative: XPath, toRelative: XPath):
    target = get(target)
    fromRelative = get(fromRelative)
    toRelative = get(toRelative)
    assert target.is_relative_to(fromRelative)
    return toRelative.joinpath(target.relative_to(fromRelative))


def openPath(path: XPath):
    os.system(f'start explorer {path}')


def _remove(*paths: XPath):
    for path in paths:
        path = get(path)
        if path.is_file():
            path.unlink(True)
        elif path.is_dir():
            shutil.rmtree(path)


async def remove(*paths: XPath):
    return await runThread(
        lambda: _remove(*paths)
    )


def _make(*paths: XPath):
    for path in paths:
        path = get(path)
        path.mkdir(parents=True, exist_ok=True)


async def make(*pathList: XPath):
    return await runThread(
        lambda: _make(*pathList)
    )


def _clearDir(*dirList: XPath):
    for dir in dirList:
        _remove(*[x for x in get(dir).iterdir()])


async def clearDir(*dirList: XPath):
    return await runThread(
        lambda: _clearDir(*dirList)
    )


def _copy(src: XPath, dst: XPath):
    src = get(src)
    dst = get(dst)
    _make(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


async def copy(src: XPath, dst: XPath):
    return await runThread(
        lambda: _copy(src, dst)
    )


def _copyMany(dataDict: dict[XPath, XPath]):
    for src, dst in dataDict.items():
        _copy(src, dst)


async def copyMany(dataDict: dict[XPath, XPath]):
    return await runThread(
        lambda: _copyMany(dataDict)
    )


def _move(src: XPath, dst: XPath, force: bool = False):
    src = get(src)
    dst = get(dst)
    if dst.exists():
        if force:
            _remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    _make(dst.parent)
    os.rename(src, dst)


async def move(src: XPath, dst: XPath, force: bool = False):
    return await runThread(
        lambda: _move(src, dst, force)
    )


def _moveMany(dataDict: dict[XPath, XPath], force: bool = False):
    for src, dst in dataDict.items():
        _move(src, dst, force)


async def moveMany(dataDict: dict[XPath, XPath], force: bool = False):
    return await runThread(
        lambda: _moveMany(dataDict, force)
    )


def renameName(src: XPath, name: str):
    src = get(src)
    src.rename(src.with_name(name))


def renameStem(src: XPath, stemName: str):
    src = get(src)
    src.rename(src.with_stem(stemName))


def renameSuffix(src: XPath, suffixName: str):
    src = get(src)
    src.rename(src.with_suffix(suffixName))


def _listPath(path: XPath, recursive: bool = False):
    '获取指定路径下文件以及目录列表'
    path = get(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


async def listPath(path: XPath, recursive: bool = False):
    return await runThread(
        lambda: _listPath(path, recursive)
    )


def _listFile(path: XPath, recursive: bool = False):
    '获取指定路径下文件列表'
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


async def listFile(path: XPath, recursive: bool = False):
    return await runThread(
        lambda: _listFile(path, recursive)
    )


def _listDir(path: XPath, recursive: bool = False):
    '获取指定路径下目录列表'
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))


async def listDir(path: XPath, recursive: bool = False):
    return await runThread(
        lambda: _listDir(path, recursive)
    )


@asynccontextmanager
async def useTempFile():
    file = tempFile()
    try:
        yield file
    finally:
        await remove(file)


@asynccontextmanager
async def useTempPath(isMakePath: bool = False):
    path = tempPath()
    if isMakePath:
        await make(path)
    try:
        yield path
    finally:
        await remove(path)


@asynccontextmanager
async def usePath(path: XPath):
    path = Path(path)
    currentPath = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(currentPath)
