# itertools提供了非常有用的用于操作迭代对象的函数

import itertools
naturals = itertools.count(1)  # 创建一个无限迭代器，从1开始计数
for n in naturals:
    print(n)
    if n >= 10:
        break   
    # 因为count()会创建一个无限的迭代器，所以上述代码会打印出自然数序列，根本停不下来，
    # 只能按Ctrl+C退出。

# cycle()会把传入的一个序列无限重复下去：
cs  = itertools.cycle('ABC')  # 创建一个无限迭代器，重复'A', 'B', 'C'
for c in cs:
    print(c)
    if c == 'C':
        break


# repeat()负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数：
ns = itertools.repeat('A', 3)  # 创建一个迭代器，重复'A'三次
for n in ns:
    print(n)

# 无限序列只有在for迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，它不会事先把无限个元素生成出来
# 无限序列虽然可以无限迭代下去，但是通常我们会通过takewhile()等函数根据条件判断来截取出一个有限的序列：

naturals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, naturals)  # �取小于等于10的自然数
print(list(ns))  # 输出：[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# chain()可以把一组迭代对象串联起来，形成一个更大的迭代器：
for c in itertools.chain('ABC', 'XYZ'):
    print(c)  # 输出：A B C X Y Z
    


# groupby()把迭代器中相邻的重复元素挑出来放在一起：

for key, group in itertools.groupby('AAABBBCCAAA'):
    print(key, list(group))  # 输出：A ['A', 'A', 'A'] B ['B', 'B', 'B'] C ['C', 'C'] A ['A', 'A', 'A']     
    
    
# 实际上挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等，
# 这两个元素就被认为是在一组的，而函数返回值作为组的key。
# 如果我们要忽略大小写分组，就可以让元素'A'和'a'都返回相同的key：
for key, group in itertools.groupby('AaaBBbcCAAa', lambda c: c.upper()):
    print(key, list(group))  # 输出：A ['A', 'a', 'a'] B ['B', 'B', 'b'] C ['C'] A ['A', 'A', 'a']  
