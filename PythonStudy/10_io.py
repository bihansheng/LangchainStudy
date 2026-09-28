#open() 读文件      'r' 表示只读，如果文件不存在会报错IOError
#read 会一次性把文件全读出来，
 #f.close() 关闭文件
def read_file(filename):
    try:
        f = open(filename, 'r')
        content = f.read()
        print(content)
    finally:
        if f:
            f.close()
            
            
#Python引入了with语句来自动帮我们调用close()方法：
with open('test.txt', 'r') as f:
    #小文件直接read()读取整个文件内容
    #print(f.read())
    #如果文件很大，用read()一次性读取文件可能会占用很大的内存，
    # 所以，可以反复调用read(size)方法，每次最多读取size个字节的内容。   
    #如果是配置文件，可以使用readlines读取。
    for line in f.readlines():
        print(line.strip()) # 把末尾的'\n'删掉
        

# 指定读取为二进制文件
#rb 十六进制表示的字节
f = open('/Users/michael/test.jpg', 'rb')
#指定字符编码
f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')


#写文件
# f = open('test.txt', 'w')
# f.write('Hello, world!')
# f.close()
with open('test.txt', 'w') as f:
    f.write('Hello, world!')
    
    
    
#StringIO  内存中读写str
# BytesIO 操作二进制数据
from io import StringIO

f = StringIO()
f.write('Hello, world!')
print(f.getvalue())
f.close()


#os 系统信息
import os
print(os.name) #posix  linux / mac   nt  windows
print(os.environ) #系统环境变量
print(os.environ.get('PATH')) #获取某个环境变量的值
print(os.path.abspath('.')) #查看当前目录的绝对路径
print(os.path.join(os.path.abspath('.'), 'test.txt')) #拼接路径
print(os.path.split('/Users/michael/test.txt')) #拆分路径
print(os.path.splitext('/Users/michael/test.txt')) #拆分文件名和扩展
os.mkdir('test') #创建目录
os.rmdir('test') #删除目录

#序列化 数据存在磁盘中
#pickle 序列化，类似 java的Serializable接口
#unpickling 反序列化
import pickle

data = {'name': 'Alice', 'age': 25, 'score': 88}
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

with open('data.pkl', 'rb') as f:
    data_loaded = pickle.load(f)
    print(data_loaded)
    
    
#json
#Python内置的json模块提供了非常完善的Python对象到JSON格式的转换
#dumps()方法返回一个str，内容就是标准的JSON。
# 类似的，dump()方法可以直接把JSON写入一个file-like Object。

#JSON反序列化为Python对象，用loads()或者对应的load()方法

import json

data = {'name': 'Alice', 'age': 25, 'score': 88}
json_str = json.dumps(data)
print(json_str)#'{"age": 20, "score": 88, "name": "Bob"}'
data_loaded = json.loads(json_str)
print(data_loaded)


#将json转为对象
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
        
#jsonData = {'name': 'Alice', 'age': 25, 'score': 88}
#json_str = json.dumps(jsonData)
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
student = json.loads(json_str, object_hook=dict2student)
print(student.name)
print(student.age)
print(student.score)    

