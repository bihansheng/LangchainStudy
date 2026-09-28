#try except finally 错误处理
try:
    print('try...')
    r = 10 / 0
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
print('END')    


#如果没有错误发生，可以在except语句块后面加一个else，当没有错误发生时，会自动执行else语句：

try:
    print('try...')
    r = 10 / 2
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
else:
    print('no error!')  
    
    
    
#使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，
# 比如函数main()调用bar()，bar()调用foo()，结果foo()出错了，
# 这时，只要main()捕获到了，就可以处理：
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        print('Error:', e)
    finally:
        print('finally...')

main()  



#Python内置的logging模块可以非常容易地记录错误信息：
#  logging.exception(e)

import logging

def foo2(s):
    return 10 / int(s)

def bar2(s):
    return foo2(s) * 2  

def main2():
    try:
        bar2('0')
    except Exception as e:
        logging.exception(e)
    finally:
        print('finally...')

main2()
print('END')


#raise 抛出错误 让上层方法处理错误
def foo3(s):
    n = int(s)
    if n == 0:
        raise ValueError('invalid value: %s' % s)
    return 10 / n


#断言
#assert 断言函数，表示表达式必须为真，否则程序出错，并且可以自定义错误信息。
def foo4(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n

#程序中如果到处充斥着assert，和print()相比也好不到哪去。
# 启动Python解释器时可以用-O参数来关闭assert：
#断言的开关“-O”是英文大写字母O，不是数字0。


#logging
#把print()替换为logging是第3种方式，和assert比，logging不会抛出错误，而且可以输出到文件：


