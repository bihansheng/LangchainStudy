# collections是Python内建的一个集合模块，提供了许多有用的集合类。
from collections import namedtuple, deque, defaultdict, OrderedDict

# namedtuple
# namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
# namedtuple('名称', [属性list]):
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)

# deque
# 为了高效实现插入和删除操作的双向列表，适合用于队列和栈：
# deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，这样就可以非常高效地往头部添加或删除元素。

q = deque(['a', 'b', 'c'])
q.append('d')
q.appendleft('z')
print(q)


# defaultdict
# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict：
# 除了在Key不存在时返回默认值，defaultdict的其他行为跟dict是完全一样的。

dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'value1'
print(dd['key1'])
print(dd['key2'])

# OrderedDict
# 使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。
# 如果要保持Key的顺序，可以用OrderedDict：
# OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：

od1 = OrderedDict([('a', 1), ('c', 2), ('d', 3)])
print(od1)

od = OrderedDict()
od['b'] = 3
od['a'] = 1
od['c'] = 2
print(od)   


# ChainMap
# ChainMap可以把多个dict串起来，使它们在逻辑上形成一个单一的dict。
from collections import ChainMap

a = {'x': 1, 'y': 2}
b = {'y': 3, 'z': 4}
c = ChainMap(a, b)
print(c)
print(c['x'])
print(c['y'])
print(c['z'])


#Counter
#Counter是一个简单的计数器，例如，统计字符出现的个数：
from collections import Counter
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)