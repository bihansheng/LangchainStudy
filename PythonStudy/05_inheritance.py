class Animal(object):
    def run(self):
        print('animal is running...')

class Dog(Animal):
    def run(self):
        print('dog is running...')  

class Cat(Animal):
    def run(self):
        print('cat is running...')

a = list()
b = Animal()
c = Cat()
d = Dog()
print(isinstance(a, list))
print(isinstance(b, Animal))
print(isinstance(c, Animal))
a.append(b)
a.append(c)
a.append(d)

for animal in a:
   animal.run()

def run_twice(animal):
    animal.run()
    animal.run()


for animal in a:
    run_twice(animal)



#多继承
class Mammal(object):
    pass

class Bird(object):
    pass    

class Runnable(object):
    def run(self):
        print('Running...') 

class Flyable(object):
    def fly(self):
        print('Flying...')  
        
# 肉食动物
class CarnivorousMixIn(object):
    def eat_meat(self):
        print('Eating meat...')
        
class HerbivoresMixIn(object):
    def eat_grass(self):
        print('Eating grass...')
   
   
class Cat(Mammal, Runnable):
    pass    


class Bat(Bird, Flyable):
    pass 


#可以同时拥有多个MixIn
class Dog(Mammal, Runnable, CarnivorousMixIn):
    pass

class Sheep(Mammal, Runnable, HerbivoresMixIn   ):
    pass




#静态语言 vs 动态语言
#对于静态语言（例如Java）来说，如果需要传入Animal类型，
# 则传入的对象必须是Animal类型或者它的子类，否则，将无法调用run()方法。
#对于Python这样的动态语言来说，则不一定需要传入Animal类型。
# 我们只需要保证传入的对象有一个run()方法就可以了

class Timer(object):
    def run(self):
        print('Timer start...')
t= Timer()
a.append(t)
for animal in a:
    run_twice(animal)


#type() 
#获取对象类型
type(123)==type(456)

type('abc')==str


#isinstance() 判断class的类型
print(isinstance(b, Animal))
print(isinstance(t, Animal))#False


#dir()函数 ，获得一个对象的所有属性和方法：
#hasattr 是否有属性 setattr 设置属性 getattr 获取属性 delattr 删除属性
print(dir(b))

print(hasattr(b, 'run'))
setattr(b, 'age', 5)
print(getattr(b, 'age'))
print(getattr(b, 'city', 'wuhan')) #如果没有city属性，返回默认值'wuhan'
#print(getattr(b, 'city')) #报错'Animal' object has no attribute 'city'
delattr(b, 'age')



#实例属性和类属性
# 由于Python是动态语言，根据类创建的实例可以任意绑定属性。
#千万不要对实例属性和类属性使用相同的名字，
# 因为相同名称的实例属性将屏蔽掉类属性，但是当你删除实例属性后，再使用相同的名称，访问到的将是类属性。

class Student(object):
    name = 'Student' #类属性
    def __init__(self, name):
        self.name = name #实例属性  
        
print(Student.name) #Student
s = Student('Michael')
print(s.name) #Michael
del s.name
print(s.name) #Student      
