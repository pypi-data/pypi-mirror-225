import os
import base64
from typing import Tuple
from . sessions import RestSession


class InvalidImageTypeError(Exception):
    pass


def makedirs(filepath: str) -> str:
    """为文件创建目录

    Args:
        filepath (str): 文件位置

    Returns:
        str: 返回目录位置
    """
    basedir, filename = os.path.split(filepath)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    return basedir


def touch_file(filepath: str, size: int):
    """创建一个指定大小的空文件

    Args:
        filepath (str): 文件位置
        size (int): 文件大小 单位 Byte
    """
    with open(filepath, "wb") as f:
        if size > 0:
            f.seek(size-1)
            f.write(b"\x00")


def seek_write(filepath: str, start: int, content: bytes):
    """向文件指定位置开始写入

    Args:
        filepath (str): 文件位置
        start (int): 开始位置
        content (bytes): 要写入的内容
    """
    with open(filepath, "r+b") as f:
        f.seek(start)
        f.write(content)


def split_filepath(filepath: str) -> Tuple[str, str, str]:
    """解析文件路径

    Args:
        filepath (str): 文件路径

    Returns:
        Tuple[str, str, str]: 目录，文件名，文件类型(小写)
    """
    basedir, filename = os.path.split(filepath)
    title, filetype = os.path.splitext(filename)
    return basedir, title, filetype.lower()


def _img2base64(filetype: str, content: bytes) -> bytes:
    """图片转base64

    Args:
        filetype (str): 文件类型, jpeg  png  gif
        content (bytes): 文件流

    Returns:
        bytes: base64格式的二进制流
    """
    if filetype not in ("jpeg", "png", "gif"):
        raise InvalidImageTypeError(f"该类型为'{filetype}', 目前只支持 jpeg png gif")

    prefix = f"image/{filetype.strip('.')}"
    return b'data:%s;base64,%s' % (prefix.encode("utf8"), base64.b64encode(content))


def img2base64(imgpath: str) -> bytes:
    """图片转base64

    Args:
        imgpath (str): 图片路径 

    Returns:
        bytes: base64格式的二进制流
    """
    _, _, filetype = split_filepath(imgpath)
    filetype = filetype.strip('.').lower()
    with open(imgpath, "rb") as f:
        content = f.read()
    return _img2base64(filetype, content)


def webimg2base64(url: str) -> bytes:
    """图片转base64

    Args:
        imgpath (str): url

    Returns:
        bytes: base64格式的二进制流
    """
    with RestSession(timeout=30) as session:
        res = session.get(url)
    filetype = res.headers["Content-Type"].split("/")[-1].lower()
    return _img2base64(filetype, res.content)


def img2base64v2(img: str) -> bytes:
    """图片转base64

    Args:
        imgpath (str): 图片路径 或 url

    Returns:
        bytes: base64格式的二进制流
    """
    if img.startswith("http"):
        return webimg2base64(img)

    elif os.path.exists(img):
        return img2base64(img)
