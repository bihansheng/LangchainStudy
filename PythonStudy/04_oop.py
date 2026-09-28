
#面向对象编程

class Student(object): # 这里的object是所有类最终都会继承的类
    #类似 Java 构造函数，前后分别有两个下划线，第一个参数永远是self，表示创建的实例本身，
    # 因此在__init__方法内部，就可以把各种属性绑定到self，因为self就指向创建的实例本身。
    #self 类似 java 中的 this
    #有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数，
    # 但self不需要传，Python解释器自己会把实例变量传进去


    #Python中，实例的变量名如果以__开头，
    #就变成了一个私有变量（private），只有内部可以访问，外部不能访问
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def get_name(self):
        return self.__name
    def get_score(self):
        return self.__score
    def set_name(self, name):
        self.__name = name
    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

    #类的方法
    def display(self):
        print(f"Name: {self.__name}, Score: {self.__score}")    

    def print_score(self):
        print(f'%s : %s' % (self.__name, self.__score))

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'


bart = Student('Bart Simpson', 80)
bart.print_score()
print(bart.get_grade())