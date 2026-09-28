#struct模块来解决bytes和其他二进制数据类型的转换

# struct的pack函数把任意数据类型变成bytes：
import struct
# 示例：将整数和浮点数打包成bytes
data = struct.pack('if', 1, 2.3)
print(data)

# struct的unpack函数把bytes变成相应的数据类型
unpacked_data = struct.unpack('if', data)
print(unpacked_data)    
