import math
import logging
import asyncio
from asyncio.events import AbstractEventLoop
import aiohttp
import requests
from sometools import utils
from sometools.utils.decorator import Command

logger = logging.getLogger("sometools")


class AsyncDownloader:
    chunkIndexs: list
    filesize: int
    chunk_size: int
    chunkNum: int
    completedNum: int = 0

    def __init__(self, url: str, filepath: str, thread: int, chunk_size: int = 1024*1024,
                 headers: dict = None):
        """异步/协程下载器

        Args:
            url (str): 文件url
            filepath (str): 保存为文件位置
            thread (int): 线程数
            chunk_size (int, optional): 分块大小
        """
        self.url = url
        self.filepath = filepath
        self.thread = thread
        self.chunk_size = chunk_size
        self.headers = headers

    async def __prepare(self):
        """创建占位空文件, 计算每个分块的坐标
        """
        # TODO: 使用head可能无法得到准确文件大小
        # 微博：使用head方法不会返回文件大小
        # b站：使用head方法返回大小每次都是 2097152
        res = requests.get(self.url, stream=True)
        self.filesize = int(res.headers.get("Content-Length") or 0)

        utils.files.makedirs(self.filepath)
        utils.files.touch_file(self.filepath, self.filesize)
        self.chunkNum = math.ceil(self.filesize / self.chunk_size)
        self.chunkIndexs = [i for i in range(self.chunkNum)][::-1]

    async def __download_chunk(self, index: int):
        """下载分块

        Args:
            index (int): 分块坐标
        """
        start = index * self.chunk_size
        headers = {
            "range":  f"bytes={start}-{start+self.chunk_size}",
            **self.headers
        }
        async with aiohttp.ClientSession() as session:
            res = await session.get(self.url, headers=headers)
            content = await res.read()

        utils.files.seek_write(self.filepath, start, content[:-1])
        self.completedNum += 1
        logger.info(
            f"[Download {self.completedNum}/{self.chunkNum}] {self.filepath}")

    async def __run(self):
        while self.chunkIndexs:
            index = self.chunkIndexs.pop()
            await self.__download_chunk(index)

    async def __start_all(self, loop: AbstractEventLoop):
        await self.__prepare()
        tasks = [loop.create_task(self.__run())
                 for _ in range(self.thread)]
        await asyncio.wait(tasks)

    def start(self):
        try:
            loop = asyncio.get_event_loop()
        except Exception as e:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(self.__start_all(loop))


@Command
def download(url: str, filepath: str, thread: int = 4, chunk_size: int = 1024*1024, **headers: str):
    """下载文件

    Args:
        url (str): 文件url
        filepath (str): 保存为文件位置
        thread (int, optional): 线程数
        chunk_size (int, optional): 分块大小
        timeout (int, optional): 超时时间
        headers (str): 头部, 格式为 key=value
    """
    downloader = AsyncDownloader(url, filepath, thread, chunk_size, headers)
    downloader.start()
