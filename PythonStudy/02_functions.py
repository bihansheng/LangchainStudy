
import math
from collections.abc import Iterable
import os

#函数
def my_function():
    print("Hello from my_function!")

my_function()

#空函数 pass() 什么都不做，类似 todo，也可以做条件判断空执行的方法
def empty_function():
    pass

def my_abs(x):
    if not isinstance(x,(int,float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
    
#返回多个值 原来返回值是一个tuple！
# 但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值
def my_move(x,y,step,angle = 0):
    nx = x +step * math.cos(angle)  
    ny = y +step * math.sin(angle)
    return nx,ny
x,y = my_move(100,100,60,math.pi/6)
print(x,y)
r = my_move(100,100,60)
print(r)

#定义默认参数要牢记一点：默认参数必须指向不变对象！
def add_end(l  =[]):
    l.append("end")
    return l
print(add_end([1,2.3]))
print(add_end())
print(add_end())
print(add_end([1,2.3]))
print(add_end()) #['end', 'end', 'end']

#用None这个不变对象来实现：
def add_end2(l = None):
    if l is None:
        l = []
    l.append("end")
    return l
print(add_end2())
print(add_end2())
print(add_end2())#['end']

#可变参数 传入的参数个数是可变的，可以是0个、1个或多个
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc(1,2))
nums = [1,2,3]
print(calc(*nums)) #*nums表示把nums这个list的所有元素作为可变参数传进去，这样函数就能计算出正确的结果

#关键字参数
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

person('Michael', 30)
person('Bob', 35, city='Beijing')
person('Adam', 45, gender='M', job='Engineer')

#命名关键字参数
#和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数。
def person2(name, age, *, city, job):
    print(name, age, city, job)
    
person2('Jack', 24, city='Beijing', job='Engineer')

def person3(name, age, *, city= 'wuhan', job):
    print(name, age, city, job)

person3('Jack', 24,  job='Engineer')

#要注意定义可变参数和关键字参数的语法：
#*args是可变参数，args接收的是一个tuple；
#**kw是关键字参数，kw接收的是一个dict。
#使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法。



#递归函数
def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)
print(fact(5))



#切片  取 list 或者 tuple 的部分元素
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[1:3])  # 取第2个到第3个元素,并生成一个新的list
print('原L:', L)  # 取前3个元素
print(L[:3])   # 取前3个元素
#倒着取
print(L[-2:])  # 取倒数第2个元素到最后
#tuple 也可以用切片操作，只是操作的结果仍是 tuple
T = (0, 1, 2, 3, 4, 5)
print(T[:3])  # 取前3个元素
#如果什么都不写，是原样复制一个list
print(L[:])  # 取所有元素

#字符串也可以看作成一中 list
str = 'abcdefg'  # 取前3个元素    
print(str[:3])

#迭代 java 中的 for-each 循环遍历
#当我们使用for循环时，只要作用于一个可迭代对象(Iterable，判断方法：isinstance(object, Iterable))，
# for循环就可以正常运行，而我们不太关心该对象究竟是list还是其他数据类型。 
d = {'a': 1, 'b': 2, 'c': 3}

for key in d:
    print(key)

for key, value in d.items():
    print(f'{key} : {value}')


str = 'abcde'
for ch in str:
    print(ch)


#Python内置的enumerate函数可以把一个list变成索引-元素对
list1 = [1, 2, 3, 4, 5]
for i, value in enumerate(list1):
    print(i, value)

map = [('Michael', 95,"A"), ('Bob', 75,"B"), ('Tracy', 85,"C")]
for name, score, grade in map:
    print(name, score, grade)


#列表生成式
L0 = list(range(5))
print(L0)

#生成一个list [1x1, 2x2, 3x3, ..., 10x10]
L =[]
for x in range(1, 11):
    L.append(x * x)
print(L)


L2 = [x * x for x in range(1,11)]
print(L2)

# for 最后的 if，不能在if 后加 else ，这里的 if 是筛选条件
# for 前面的 if 需要 else,这里的 if 是表达式的一部分
L3 = [x * x for x in range(1,11) if x %2 == 0]  
print(L3)

files = [d for d in os.listdir('.') if os.path.isfile(d)]
print(files)

#同时生成两个或者多个变量
dd = {'X': 'A', 'Y': 'B', 'Z': 'C'}
L4 = [k + '=' + v.lower() for k, v in dd.items()]
print(L4)   

#生成器 generator  一边循环一边计算的机制，称为生成器：generator。
#第一种方法很简单，只要把一个列表生成式的[]改成()，就创建了一个generator：
#这里是生成一个list
L5 = [x * x for x in range(10)]
print(L5) 
#这里是定义一个生成器
g = (x * x for x in range(10))
#可以通过每次调用next(g)，就计算出g的下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。
print(next(g))
print(next(g))
print(next(g))
#也可以用for 循环来迭代这个 generator，拿到每一个元素的值
for n in g:
    print(n)


#如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，
# 而是一个generator函数，调用一个generator函数将返回一个generator：
def fib(max):
    n,a,b = 0,0,1
    while n < max:
        yield b
        a,b = b,a+b
        n= n+1
    return 'done'   
f= fib(6)
for n in f:
    print(n)
#遇到yield就中断，下次又继续执行
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)
o = odd()
print(next(o))  
print(next(o))
print(next(o))

#如果这样调用next()每次都返回1：，因为每次调用odd()都会创建一个新的生成器对象   
next(odd())
next(odd())
next(odd())


#迭代器
#可以直接作用于for循环的数据类型有以下几种：
#一类是集合数据类型，如list、tuple、dict、set、str等；
#一类是generator，包括生成器和带yield的generator function。
#这些可以直接作用于for循环的对象统称为可迭代对象：Iterable。
#可以使用isinstance()判断一个对象是否是Iterable对象：
#可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
#Python的for循环本质上就是通过不断调用next()函数实现的
