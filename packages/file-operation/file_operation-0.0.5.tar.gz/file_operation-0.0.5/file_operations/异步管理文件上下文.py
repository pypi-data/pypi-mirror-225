#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:automaticoffice
# py_name :异步管理文件上下文
# software: PyCharm
# datetime:2021/2/1 19:59

import asyncio

#
# class AContext:
#     def __init__(self):
#         print("in init")
#
#     async def __aenter__(self):
#         print("in aenter")
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         print("in aexit", exc_type, exc_val, exc_tb)
#
#
# async def main():
#     async with AContext() as ac:
#         print("in with", ac)

'''
上面的代码通过使用asyncio中run_in_executor运行一个线程，来使得阻塞操作变为非阻塞操作，达到异步非阻塞的目的。
AsyncFile类提供了一些方法，这些方法将用于将write、read和readlines的调用添加到pending列表中。这些任务通过finally块中的事件循环在ThreadPoolExecutor进行调度。
yield 前半段用来表示__aenter__()
yield 后半段用来表示__aexit__()
使用finally以后可以保证链接资源等使用完之后能够关闭。
'''
# 3.7
from contextlib import asynccontextmanager
# 3.6
from async_generator import asynccontextmanager
from concurrent.futures.thread import ThreadPoolExecutor


# <editor-fold desc="写入">
class AsyncFile(object):
    def __init__(self, file, loop=None, executor=None):
        if not loop:
            loop = asyncio.get_running_loop()  # 获取当前运行事件循环
        if not executor:
            executor = ThreadPoolExecutor(10)  # 线程池数量10
        self.file = file
        self.loop = loop
        self.executor = executor
        self.pending = []
        self.result = []

    def write(self, string):
        """
        实现异步写操作
        :param string: 要写的内容
        :return:
        """
        self.pending.append(
            self.loop.run_in_executor(
                self.executor, self.file.write, string,
            )
        )

    def read(self, i):
        """
        实现异步读操作
        :param i:
        :return:
        """
        self.pending.append(
            self.loop.run_in_executor(self.executor, self.file.read, i, )
        )

    def readlines(self):
        self.pending.append(
            self.loop.run_in_executor(self.executor, self.file.readlines, )
        )


@asynccontextmanager
async def async_open(path, mode="w"):
    with open(path, mode=mode, encoding='utf8') as f:
        loop = asyncio._get_running_loop()
        file = AsyncFile(f, loop=loop)
        try:
            yield file
        finally:
            file.result = await asyncio.gather(*file.pending, loop=loop)


import tempfile
import os


async def main():
    # tempdir = tempfile.gettempdir()
    tempdir = os.getcwd()
    path = os.path.join(tempdir, "run.txt")
    print(f"临时文件目录:{path}")

    async with async_open(path, mode='w') as f:
        f.write("公众号: ")
        f.write("Python")
        f.write("学习")
        f.write("开发")


# </editor-fold>


# 同步挂起协程

# <editor-fold desc="读出">
class Sync():
    def __init__(self):
        self.pending = []
        self.finished = None

    def schedule_coro(self, coro, shield=True):
        # 如果去掉asyncio.shield，在取消fut函数的时候，就会导致coro协程也出错。
        fut = asyncio.shield(coro) if shield else asyncio.ensure_future(coro)
        self.pending.append(fut)
        return fut

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 退出async with的时候，任务列表中的任务进行并发操作。
        self.finished = await asyncio.gather(*self.pending, return_exceptions=True)


async def workload1():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 41")
    return 41


async def workload2():
    await asyncio.sleep(1)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 42")
    return 42


async def workload3():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 43")
    return 43


async def workload4():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 43")
    return 43


async def workload5():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 43")
    return 43


async def workload6():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 43")
    return 43


async def workload7():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 43")
    return 43


async def workload8():
    await asyncio.sleep(2)
    f = open('run.txt', 'r', encoding='utf8')
    data = f.read()
    print(data)
    print("These coroutines will be executed return 43")
    return 43


async def main2():
    async with Sync() as sync:
        # 使用异步上下文可以创建同步协程程序
        sync.schedule_coro(workload1())
        sync.schedule_coro(workload2())
        sync.schedule_coro(workload3())
        sync.schedule_coro(workload4())
        sync.schedule_coro(workload5())
        sync.schedule_coro(workload6())
        sync.schedule_coro(workload7())
        sync.schedule_coro(workload8())
    print("All scheduled corotines have retuned or throw:", sync.finished)


# </editor-fold>


if __name__ == '__main__':
    data = """
    E:\virtualenvs\automaticoffice\Scripts\python.exe F:/jiyiproj/automaticoffice/002common/文件以及文件夹/异步管理文件上下文.py
start
公众号: Python学习开发
These coroutines will be executed return 42
公众号: Python学习开发
These coroutines will be executed return 43
公众号: Python学习开发
These coroutines will be executed return 43
公众号: Python学习开发
These coroutines will be executed return 43
公众号: Python学习开发
These coroutines will be executed return 43
公众号: Python学习开发
These coroutines will be executed return 43
公众号: Python学习开发
These coroutines will be executed return 41
公众号: Python学习开发
These coroutines will be executed return 43
All scheduled corotines have retuned or throw: [41, 42, 43, 43, 43, 43, 43, 43]

Process finished with exit code 0
    """
    for i in range(1000):
        print(1)
        f = open('run.txt', 'a', encoding='utf8')
        f.write(data + '\n')
    print("start")
    # Python 3.6
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_until_complete(main2())
    # Python 3.7
    # asyncio.run(main())
