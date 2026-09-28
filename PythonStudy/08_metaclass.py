#元类

#type()
#动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的。

#type()函数可以查看一个类型或变量的类型，Hello是一个class，它的类型就是type，而h是一个实例，它的类型就是class Hello。

class Hello:
    def hello(self, name='world'):
        print('Hello, %s.' % name)  
        
h = Hello()
print(type(Hello)) #<class 'type'>
print(type(h)) #<class '__main__.Hello'>