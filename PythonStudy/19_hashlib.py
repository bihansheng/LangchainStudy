# hashlib提供了常见的哈希算法，如MD5，SHA1等等

import hashlib

md5 = hashlib.md5()
md5.update("hello world".encode("utf-8"))
print(md5.hexdigest())  # 输出：5eb63bbbe01eeed093

# 如果数据量很大，可以分块多次调用update()，最后计算的结果是一样的：

md5 = hashlib.md5()
md5.update("hello ".encode("utf-8"))
md5.update("world".encode("utf-8"))
print(md5.hexdigest())  # 输出：5eb63bbbe01eeed093

# 另一种常见的哈希算法是SHA1，调用SHA1和调用MD5完全类似：

sha1 = hashlib.sha1()
sha1.update("hello world".encode("utf-8"))
print(sha1.hexdigest())  # 输出：2aae6c35c94fce5dbb8f7f0c2e0b6c9d   
