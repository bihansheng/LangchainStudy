"""
字符串解析器StrOutputParser
它是LangChain中最简单的输出解析器，它可以简单地将任何输入转换为字符串。
从结果中提取content字段转换为字符串输出。
"""

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from loguru import logger

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

# 初始化聊天模型
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_retries=2,
)

# 创建聊天提示模板，包含系统角色设定和用户问题输入
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个{role}，请简短回答我提出的问题，结果返回json格式，q字段表示问题，a字段表示答案。",
        ),
        ("human", "请回答:{question}"),
    ]
)

# 使用指定的角色和问题生成具体的提示内容
prompt = chat_prompt.invoke(
    {"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"}
)
print(prompt)

# 调用模型获取回答结果
result = model.invoke(prompt)
print(" ========== 模型原始输出 ============")
print(f"模型原始输出:\n{result}")
print("\n")

print(" ========== 1 、StrOutputParser.invoke(result)  解析返回结果 ============")
# 创建字符串输出解析器，用于解析模型返回的结果
parser = StrOutputParser()
response = parser.invoke(result)
print(f"StrOutputParser解析后的结构化结果:\n{response}")
print(f"结果类型: {type(response)}")
print("\n")


print(" ========== 2、JsonOutputParser.invoke(result)  解析返回结果  ============")

# 创建JSON输出解析器实例
parser2 = JsonOutputParser()
try:
    # 这里可能会因为类型不对导致解析报错
    response2 = parser2.invoke(result)
    print(f"解析后的结构化结果:\n{response2}")
    print(f"结果类型: {type(response2)}")  # <class 'dict'>
    print("\n")
except Exception as e:  # noqa: BLE001
    logger.error(f"配置错误：{e!s}")


from pydantic import BaseModel, Field

# 先在ChatPromptTemplate中指定JsonOutputParser.get_format_instructions，
# 得到模型返回数据后使用JsonOutputParser.invoke(result)  解析返回结果
print(
    " ==============3、在format中指定JsonOutputParser的输出结果类对象================="
)


class Person(BaseModel):
    time: str = Field(description="时间")
    person: str = Field(description="人物")
    event: str = Field(description="事件")


# 创建JSON输出解析器，用于将model输出解析为Person对象
parser2 = JsonOutputParser(pydantic_object=Person)

# 获取格式化指令，告诉model如何输出符合要求的JSON格式
format_instructions2 = parser2.get_format_instructions()

# 创建聊天提示模板，定义系统角色和用户输入格式
chat_prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手，你只能输出结构化JSON数据。"),
        ("human", "请生成一个关于{topic}的新闻。{format_instructions}"),
    ]
)

# 格式化提示词，指定 返回数据的格式
prompt2 = chat_prompt2.format_messages(
    topic="小米su7跑车", format_instructions=format_instructions2
)
# 记录格式化后的提示词信息
print(f"方法 3 格式化后的提示词信息:\n{prompt2}")
# 调用大语言模型获取响应结果
result2 = model.invoke(prompt2)
print(f"方法 3 ：模型原始输出:\n{result2}")
response2 = parser.invoke(result2)
print(f"方法 3 ：解析后的结构化结果:\n{response2}")
print(f"方法 3 ：结果类型: {type(response2)}")


from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, field_validator

"""
PydanticOutputParser 是 LangChain 输出解析器体系中最常用、最强大的结构化解析器之一。
它与 JsonOutputParser 类似，但功能更强 —— 能直接基于 Pydantic 模型 定义输出结构，
并利用其类型校验与自动文档能力。
对于结构更复杂、具有强类型约束的需求，PydanticOutputParser 则是最佳选择。
它结合了Pydantic模型的强大功能，提供了类型验证、数据转换等高级功能
"""


print(" =======4、PydanticOutputParser 指定返回数据对象类型 =========")

# 先在ChatPromptTemplate 指定PydanticOutputParser.get_format_instructions，
# 得到模型返回数据后使用PydanticOutputParser.invoke(result)  解析返回结果


class Product(BaseModel):
    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10:
            raise ValueError("产品简介长度必须大于等于10")
        return value


# 创建Pydantic输出解析器实例，用于解析模型输出为Product对象
parser3 = PydanticOutputParser(pydantic_object=Product)

# 获取格式化指令，用于指导模型输出符合Product模型的JSON格式
format_instructions3 = parser3.get_format_instructions()

# 创建聊天提示模板，包含系统消息和人类消息
prompt_template3 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手，你只能输出结构化的json数据\n{format_instructions}"),
        ("human", "请你输出标题为：{topic}的新闻内容"),
    ]
)

# 格式化提示消息，填充主题和格式化指令
prompt3 = prompt_template3.format_messages(
    topic="华为Mate X7", format_instructions=format_instructions3
)
# 记录格式化后的提示消息
print(f"方法 4 格式化后的提示消息:\n{prompt3}")
# 调用模型获取结果
result3 = model.invoke(prompt3)
# 记录模型返回的结果
print(f"方法 4 ：模型原始输出:\n{result3.content}")
# 使用解析器将模型结果解析为Product对象
response3 = parser3.invoke(result3)
print(f"方法 4 ：解析后的结构化结果:\n{response3}")
print(f"方法 4 ：结果类型: {type(response3)}")


print(
    " =================5、使用with_structured_output 指定数组格式 ====================="
)
# 直接使用 model.with_structured_output 指定返回数据格式
# llm_with_structured_output.invoke 真正执行模型调用
# 感觉这种写法更简洁

from typing import Annotated, TypedDict


class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]


class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"]  # List<Animal>


messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}]

llm_with_structured_output = model.with_structured_output(AnimalList)
resp = llm_with_structured_output.invoke(messages)
print(resp)
