#多进程
from multiprocessing import Process

#Unix/Linux操作系统提供了一个fork()系统调用，它非常特殊。
# 普通的函数调用，调用一次，返回一次，但是fork()调用一次，返回两次，
# 因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），
# 然后，分别在父进程和子进程内返回。

def worker(num):
    print(f'Worker: {num}')

if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = Process(target=worker, args=(i,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
        
        
#Pool如果要启动大量的子进程，可以用进程池的方式批量创建子进程：

from multiprocessing import Pool

def worker_pool(num):
    print(f'Worker Pool: {num}')

if __name__ == '__main__':
    with Pool(5) as p:
        p.map(worker_pool, range(5))

#子进程
#subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出。

import subprocess

# 启动一个子进程
print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)

#如果子进程还需要输入，则可以通过communicate()方法输入：
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)

#进程间通信
# Process之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。
# Python的multiprocessing模块包装了底层的机制，提供了Queue、Pipes等多种方式来交换数据。
# 以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据：
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
