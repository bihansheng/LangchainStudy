#协程
# 子程序调用是通过栈实现的，一个线程就是执行一个子程序。
# 最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

# 第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

# 用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：

import time, threading

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)


# asyncio的编程模型就是一个消息循环。
# asyncio模块内部实现了EventLoop，把需要执行的协程扔到EventLoop中执行，就实现了异步IO。
# asyncio是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。

import asyncio

async def hello():
    print("Hello world!")
    # 异步调用asyncio.sleep(1):
    # 把asyncio.sleep(1)看成是一个耗时1秒的IO操作，
    # 在此期间，主线程并未等待，而是去执行EventLoop中其他可以执行的async函数了，
    # 因此可以实现并发执行。
    await asyncio.sleep(1)
    print("Hello again!")

# async把一个函数变成coroutine类型，
# 然后，我们就把这个async函数扔到asyncio.run()中执行。
asyncio.run(hello())
 
 
 
 # 传入name参数:
async def hello(name):
    # 打印name和当前线程:
    print("Hello %s! (%s)" % (name, threading.current_thread))
    # 异步调用asyncio.sleep(1):
    await asyncio.sleep(1)
    print("Hello %s again! (%s)" % (name, threading.current_thread))
    return name

async def main():
    # 用asyncio.gather()同时调度多个async函数：
    L = await asyncio.gather(hello("Bob"), hello("Alice"))
    print(L)
    
asyncio.run(main())
# Hello Bob! (<function current_thread at 0x104de3880>)
# Hello Alice! (<function current_thread at 0x104de3880>)
# Hello Bob again! (<function current_thread at 0x104de3880>)
# Hello Alice again! (<function current_thread at 0x104de3880>)
# ['Bob', 'Alice']