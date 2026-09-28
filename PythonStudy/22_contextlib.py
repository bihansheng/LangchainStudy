# 在Python中，读写文件这样的资源要特别注意，必须在使用完毕后正确关闭它们。
# 正确关闭文件资源的一个方法是使用try...finally：
try:
    f = open('somefile.txt', 'r')
    # 进行文件操作
finally:
    f.close()
    
# 但是如果在文件操作中发生了异常，finally语句块中的f.close()仍然会被执行，
# 这样就保证了文件资源被正确关闭。

# 使用with语句可以更简洁地实现同样的功能：
with open('somefile.txt', 'r') as f:
    # 进行文件操作
     f.read()
# 文件操作结束后，文件会被自动关闭，即使发生异常也会如此。


# 并不是只有open()函数返回的fp对象才能使用with语句。
# 实际上，任何对象，只要正确实现了上下文管理，就可以用于with语句。

#  @contextmanager
# @contextmanager这个decorator接受一个generator，
# 用yield语句把with ... as var把变量输出出去，然后，with语句就可以正常地工作了：


from contextlib import contextmanager
class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...' % self.name)

@contextmanager
def create_query(name):
    print('Begin')
    q = Query(name)
    yield q
    print('End')

with create_query('Bob') as q:
    q.query()


#很多时候，我们希望在某段代码执行前后自动执行特定代码，也可以用@contextmanager实现。例如：
@contextmanager
def tag(name):
    print("<%s>" % name)
    yield
    print("</%s>" % name)

with tag("h1"):
    print("hello")
    print("world")

# @closing
# 如果一个对象没有实现上下文，我们就不能把它用于with语句。
# 这个时候，可以用closing()来把该对象变为上下文对象。
# 例如，用with语句使用urlopen()：
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('http://www.python.org')) as page:
    for line in page:
        print(line)

# closing也是一个经过@contextmanager装饰的generator，这个generator编写起来其实非常简单：
@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()
