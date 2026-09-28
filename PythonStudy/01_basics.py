
# 第一课 Python 基础
print("holle word")
a = 100
if a > 0:
    print("a is positive")
else:
    print("a is negative")  

#print 多行
print('''a
b
c''')

print('''hello \n
      world''')

#布尔值
print(True)
print(not False)
print(1 > 2)
print(1 < 2)
print(1 == 2 and 1 < 2)

#变量
a = 'abc'
b = a
a = 'cde'
print(a)
print(b)

#除法精度,
# Python的浮点数也没有大小限制，但是超出一定范围就直接表示为inf（无限大）。
print(10 / 3)
print(9 / 3)
print(10 // 3)

#编码
print('abc'.encode('ascii') )
print('中文'.encode('utf-8') )
#print('中文'.encode('ascii') )

#格式化
print('Hello, %s' % 'world')
print('Hi, %s, you have $%d.' % ('Michael', 1000000))
print('%.2f' % 3.1415926)
#format()

# list
classmates =["aa","bb","cc"]
print(classmates)
print(len(classmates))
print(classmates[2])
print(classmates[-1])
classmates.append("dd")
print(classmates)
classmates.insert(1,"ee")
print(classmates)
classmates.pop()
print(classmates)
print('pop(1):', classmates.pop(1))
print(classmates)

#tuple 元组 和 list 非常相似，但是元组一旦初始化就不能修改
tuple1 = (1, 2, 3)
print(tuple1)
tuple2 = (1,)
print(tuple2)

#条件判断,注意不要少写了冒号:
age = 20
if age >= 18 :
    print('adult')
    print('your age is ',age)   
elif age >= 6 :
    print('teenager')
    print('your age is ',age)
else:
    print('kid')

#非 0 数字，非空字符串，非空 list，非空 tuple 等等都算 True，其他的都算 False。
if not '' :
    print('False')

if not 0 :
    print('False')

# input
# birthday  = input('birth: ')
# if int(birthday) < 2000 :
#     print('00前')
# else:
#     print('00后')


#匹配

age = 2

match age:
    case 0:
        print('0')
    case 1:
        print('1')
    case 2:
        print('2')
    case _:
        print('other')

match age:
    case 0 | 1 | 2:
        print('0,1,2')
    case x if x < 10:
        print('x < 10')
    case _:
        print('other')

#可以匹配列表
arge = ['green', 'yellow']
match arge:
    case ['green', 'yellow', 'red']:
        print('traffic 3333')
    case ['green', 'yellow']:
        print('traffic 2222')
    case ['green']:
        print('traffic 11111')
    case _:
        print('other')

#循环 for x in list
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)

nums = [1, 2, 3, 4, 5,6, 7, 8, 9]
sum = 0
for i in nums:
    sum = sum + i
print(sum)

#range() 生成一个整数序列，可以通过list()函数转换为list
list2 = list(range(5))
print(list2)

list2 = list(range(1, 10, 2))
print(list2)

sum = 0
for x in list2 :
    sum = sum + x
print(sum)

#while 循环
sum = 0
n= 9 
while n > 0:
    sum = sum + n
    n = n - 1   
print(sum)

#break 语句可以提前退出循环
#continue 语句可以直接继续下一轮循环，跳过当前的这轮循环。


#dict 字典 java 中的 map,
# dict 的 key 必须是不可变对象。list 是可变对象，就不能作为 key。
# 查询和插入快，但内存占用大
data = {"name": "Michael", "age": 20, "score": 88}
print(data["name"])
data['score'] = 99
print(data['score'])
print(data.get('name11','default value'))
data.pop('age')
print(data)


#set dict，也是一组 key，但是没有 value，而且 key 不能重复,无序
# key 也是不可变量，由于没有 value，它 更接近java中的字典
s= {1, 2, 3}   
print(s)
#使用 list初始化 set
s = set([1, 2, 3])
print(s)
#自动过滤重复
s = set([1, 3,3, 2, 1])
print(s)

#对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。
# 相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。