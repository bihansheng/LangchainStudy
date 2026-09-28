#函数式  理解为面向过程编程
#函数本身也可以赋值给变量，即变量可以指向函数
#函数名 就是指向函数的变量

#高阶函数
#一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数。

f = abs
print(f(-10))
def add(x,y,f):
    return f(x) +f(y)   
print(add(-5,6,abs))

#高阶函数：map 
# 使用 f 执行 list 中的每一个元素，并把结果作为新的Iterator返回
def f(x):
    return x * x
r = map(f, [1,2,3,4,5,6])
print(list(r))

#高阶函数:reduce 
# 把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，
# reduce把结果继续和序列的下一个元素做累积计算
from functools import reduce
def add(x,y):
    return x * 10 + y
print(reduce(add, [1,3,5,7,9])) 


DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def char2num(s):
    return DIGITS[s]
def str2int(s):
    return reduce(add, map(char2num, s))

print(str2int('9876543210'))


#filter() 过滤函数
#filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
#注意到filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果，
#需要用list()函数获得所有结果并返回list
def is_odd(n):
    return n % 2 == 1
print(list(filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9])))

#sorted() 排序函数
#sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序：
print(sorted([36, 5, -12, 9, -21], key=abs))
#字符串排序
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True))
#忽略大小写的排序

L5 = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
    return t[0].lower()
def by_score(t):
    return t[1]
print(sorted(L5, key=by_name))
print(sorted(L5, key=by_score, reverse=True))   


#返回函数
# 高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。

def calc_sum(*args):
    ax = 0
    for n in args:
        ax = ax + n
    return ax
print(calc_sum(1, 3, 5, 7, 9))  
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax +n
        return ax
    return sum
f = lazy_sum(1, 3, 5, 7, 9)
print(f())

#返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。
#nonlocal
#使用闭包，就是内层函数引用了外层函数的局部变量。如果只是读外层变量的值，我们会发现返回的闭包函数调用一切正常：
def inc():
    x = 0
    def fn():
        return x + 1
    return fn
f = inc()
print(f())
print(f())
print(f())
#但是，如果对外层变量赋值，由于Python解释器会把x当作函数fn()的局部变量，它会报错：
#原因是x作为局部变量并没有初始化，直接计算x+1是不行的。
#使用闭包时，对外层变量赋值前，需要先使用nonlocal声明该变量不是当前函数的局部变量。

def inc():
    x = 0
    def fn():
        nonlocal x
        x = x + 1
        return x
    return fn

f2 = inc()
print(f2()) 
print(f2())
print(f2())

#匿名函数
#当我们在传入函数时，实际上也可以传入匿名函数。
print(list(map(lambda x:x*x , [1, 2, 3, 4, 5, 6, 7, 8, 9])))

#匿名函数 lambda x: x * x 实际上就是：
def f(x):
    return x * x
#关键字 lambda 表示匿名函数，冒号前面的 x 表示函数参数。
#例如，等价的匿名函数写法为：
g = lambda x: x * x
print(g(5))

def build(x, y):
    return lambda: x * x + y * y
f = build(3, 4)
print(f())  # 25

#Python对匿名函数的支持有限，只有一些简单的情况下可以使用匿名函数。


#装饰器 在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
#通过 Python 的@语法，把构造器置在函数的定义处，等于执行了语句 now = log(now)，即把now函数变成了经过装饰的函数。
@log
def now():
    print('2015-3-25')
now()

#如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute')
def now():
    print('2015-3-25')
now()

#偏函数
#通过设定参数的默认值，可以降低函数调用的难度。而偏函数也可以做到这一点
#functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
import functools

def my_int(arg1, arg2):
    return  arg1 % arg2
my_int2 = functools.partial(my_int, 2)
print(my_int2(15))  # 1

int2 = functools.partial(int, base=2)
print(int2('1000000'))  # 64
print(int2('1010101'))  # 85    