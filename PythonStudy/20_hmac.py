# Hmac算法：Keyed-Hashing for Message Authentication。
# 它通过一个标准算法，在计算哈希的过程中，把key混入计算过程中

# 使用hmac和普通hash算法非常类似。hmac输出的长度和原始哈希算法的长度一致。
# 需要注意传入的key和message都是bytes类型，str类型需要首先编码为bytes。

import hmac
import hashlib
message = b'Hello, world!'
key = b'secret'
h = hmac.new(key, message, digestmod=hashlib.sha256)
print(h.hexdigest())  # 输出：d2a1f0e5b8    