#Python的class中还有许多这样有特殊用途的函数，可以帮助我们定制类
##__str__()  __repr__()  __iter__()  __getitem__()  __getattr__()  __call__()


#定义一个特殊的__slots__变量，来限制该class实例能添加的属性：
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

s = Student() #创建新的实例
s.name = 'Michael' #绑定属性'name'
s.age = 25 #绑定属性'age'
#s.score = 99 #绑定属性'score'，报错，AttributeError: 'Student' object has no attribute 'score'


#__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的：
class GraduateStudent(Student):
        pass
    
g = GraduateStudent()
g.score = 99 #绑定属性'score'，没有报错


#Python内置的@property装饰器就是负责把一个方法变成属性调用
class Student2(object):
    @property #get 相当于把方法score()变成属性调用get_score()
    def score(self):
        return self._score

    @score.setter #set 相当于把方法score()变成属性调用set_score()
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
        
    @property
    def birth(self):
        return self._birth
        
s2 =Student2()
s2.score = 60 #实际转化为s.set_score(60)
print(s2.score) #实际转化为s.get_score()    
# 只设置property的getter方法，不定义setter方法就是一个只读属性：
# s2.birth = 1990 #实际转化为s.set_birth(1990)
# print(s2.birth) #实际转化为s.get_birth()，没有setter方法，所以birth属性是只读属性



#__str__()
class Student3(object):
    def __init__(self, name):
        self.name = name

    #java中toString()方法的作用就是把一个对象变成字符串，
    #在Python中，使用__str__()方法来实现这个功能。
    def __str__(self):
        return 'Student object (name: %s)' % self.name
    #__repr__() 的作用和__str__()一样，都是把一个对象变成字符串，
    #不同的是__str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，
    # 也就是说，__repr__()是为调试服务的。
print(Student3('Michael')) #打印的是对象的地址


#__iter__
#如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，
#该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，
#直到遇到StopIteration错误时退出循环。
class Fib(object):
    def __init__(self):
        self.a , self.b = 0 ,1 
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self.a , self.b = self.b , self.a + self.b
        if self.a > 1000:
            raise StopIteration()
        return self.a
    
for n in Fib():
    print(n)
    
    
#__getitem__
#Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行，比如，取第5个元素：
#f = Fib()
#print(f[5]) #报错，TypeError: 'Fib' object is not subscriptable


#要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
class Fib2(object):
    def __getitem__(self, n):
       if isinstance(n, int): #n是索引
           a, b = 1, 1
           for x in range(n):
               a, b = b, a + b
           return a
       if isinstance(n, slice): #n是切片
           start = n.start
           stop = n.stop    
           a, b = 1, 1
           L = []
           for x in range(stop):
               if x >= start:
                   L.append(a)
               a, b = b, a + b
           return L
       
print(Fib2()[0:5]) # [1, 1, 2, 3, 5]
print(Fib2()[:10]) # [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


#__getattr__  动态返回一个属性
#正常情况下，当我们调用类的方法或属性时，如果不存在，就会报错，
 
class Student4(object):
    def __init__(self):
        self.name = 'Michael'   
    
    def __getattr__(self, attr):
        if attr == 'score':
            return 99
        if attr == 'age':
            return lambda: 25 #返回函数也是可以的
        raise AttributeError('\'Student4\' object has no attribute \'%s\'' % attr)  
    
print(Student4().score) # 99
print(Student4().age()) # 25

#__call__ 
#一个对象实例可以有自己的属性和方法，当我们调用实例方法时，我们用instance.method()来调用。
#如果直接在实例本身上调用，就需要实现__call__()方法
class Student5(object):
    def __init__(self, name):
        self.name = name
        
    def __call__(self):
        print('My name is %s.' % self.name) 

s = Student5('Michael')
s()  # My name is Michael.  
#那么，怎么判断一个变量是对象还是函数呢？其实，更多的时候，我们需要判断一个对象是否能被调用，
# 能被调用的对象就是一个Callable对象，比如函数和我们上面定义的带有__call__()的类实例：
import collections.abc
print(isinstance(s, collections.abc.Callable))  # True  