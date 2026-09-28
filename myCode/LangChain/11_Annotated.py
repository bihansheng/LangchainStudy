# 类型强校验对象
from typing import Annotated, TypedDict

Age = Annotated[int, "年龄，范围0-150"]


class Person(TypedDict):
    name: str
    age: int
    age2: Age  # type: ignore


p = Person(name="z3", age=111, age2=188)
print(p)

# p = Person(name="z3",age="1111")
# print(p)

"""
一、核心原因 1：Annotated 本身不具备运行时校验能力
typing.Annotated的设计目的并不是在程序运行时对数据进行合法性校验（比如范围、格式检查），它的核心作用是：
为类型添加元数据（附加描述信息）：你这里的"年龄，范围0-150"就是元数据，仅用于说明、文档生成、静态分析工具识别等场景，不会被 Python 解释器在运行时解析和执行校验逻辑。
保留原始类型特性：Annotated[int, "年龄，范围0-150"]本质上还是int类型，Python 运行时只会校验它是否是int类型（这里 188 是合法int），不会关心附加的元数据内容。
简单说：Annotated只是给类型 “加注释”，不是给类型 “加校验规则”。

二、核心原因 2：Python 的类型提示（Type Hints）是静态的、仅供参考的（装饰性）
"""


# ======================= 一般使用 BaseModel 定义类型强校验 对象======================
from typing import Annotated

from pydantic import BaseModel, Field, ValidationError

# 用Annotated结合Field设置范围约束，兼具注释和运行时校验能力
Age = Annotated[int, Field(ge=0, le=150, description="年龄，范围0-150")]


class Person(BaseModel):
    name: str
    age: int
    age2: Age  # type: ignore


try:
    p = Person(name="z3", age=11, age2=188)
    print(p)
except ValidationError as e:
    print("数据校验失败：")
    print(e)


# =======================  另一种写法  ======================
class Person(BaseModel):
    """
    定义一个新闻结构化的数据模型类
    属性:
        time (str): 新闻发生的时间
        person (str): 新闻涉及的人物
        event (str): 发生的具体事件
    """

    time: str = Field(description="时间")
    person: str = Field(description="人物")
    event: str = Field(description="事件")
