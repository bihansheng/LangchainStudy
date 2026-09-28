"""
虽然大模型具备强大的语言理解和生成能力，但它本质上是静态的、不可交互的
LangChain内置工具列表 https://docs.langchain.com/oss/python/integrations/tools

通过 Tool（工具）机制，可以让模型具备“调用外部函数”的能力，使其能够与外部系统、API 或自定义函数交互，从而完成仅靠文本生成无法实现的任务
ToolCalling(也称为FunctionCalling)它允许大模型与一组API或工具进行交互，将 LLM 的智能与外部工具或 API无缝连接，从而增强大模型其功能。
"""


# 自定义 Tool
# 使用@tool装饰器

# from json import tool


# @tool
# def add_number(a: int, b: int) -> int:
#     """两个整数相加"""
#     return a + b

# result = add_number.invoke({"a": 1, "b": 12})
# print(result)

# print()

# print(f"{add_number.name=}\n{add_number.description=}\n{add_number.args=}")

from langchain.tools import tool

"""
使用@tool装饰器
装饰器默认使用函数名称作为工具名称，但可以通过参数name_or_callable 来覆盖此设置。
同时，装饰器将使用函数的文档字符串作为工具的描述，因此函数必须提供文档字符串
"""

"""
需求：
定义了一个名为add_number的工具函数，用于执行两个整数相加操作。主要功能包括：

使用Pydantic定义参数模型FieldInfo，指定两个整数参数a和b
通过@tool装饰器将函数注册为LangChain工具，绑定参数schema
打印工具的元信息（名称、参数、描述等）并调用工具执行加法运算并输出结果
"""
from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field

# 使用Pydantic定义参数模型FieldInfo，指定两个整数参数a和b
"""
public class FieldInfo {
    private final int a;//第1个参数
    private final int b;//第2个参数
    public FieldInfo(int a, int b) {
        this.a = a;
        this.b = b;
    }
    //=====getter=====
}
"""


class FieldInfo(BaseModel):
    """
    定义加法运算所需的参数信息
    """

    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")


# 通过args_schema定义参数信息，也可以定义name、description、return_direct参数
@tool(args_schema=FieldInfo)
def add_number(a: int, b: int) -> int:
    return a + b


# 打印工具的基本信息
logger.info(f"name = {add_number.name}")
logger.info(f"args = {add_number.args}")
logger.info(f"description = {add_number.description}")
logger.info(f"return_direct = {add_number.return_direct}")

# 调用工具执行加法运算
res = add_number.invoke({"a": 1, "b": 2})
logger.info(res)


# =================== 查询天气 =======================

from langchain_core.tools import tool
import json
import os
import httpx


@tool
def get_weather(loc):
    """
    查询即时天气函数

    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
                则 loc 参数需要输入 'Beijing'/'shanghai'。
    :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
             https://home.openweathermap.org/users/sign_in。
             返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式进行表示，
             其中包含了全部重要的天气信息。
    """
    # Step 1. 构建请求 URL
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2. 设置查询参数，包括城市名、API Key、单位和语言
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
        # "appid": "fc19f7b552b4c1ae467e36fe6955666",  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn",  # 输出语言为简体中文
    }

    # Step 3. 发送 GET 请求获取天气数据
    response = httpx.get(url, params=params, timeout=30)

    # Step 4. 解析响应内容为 JSON 并序列化为字符串返回
    data = response.json()
    # print(json.dumps(data))
    return json.dumps(data)


# 测试
# result = get_weather.invoke("shanghai")
result = get_weather.invoke("beijing")
print(result)
