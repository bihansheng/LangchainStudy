# PromptTemplate
# 针对文本生成模型的提示词模板，也是LangChain提供的最基础的模板，通过格式化字符串生成提示词，在执行invoke时将变量格式化到提示词模板中

# 主要参数：
#   1、template：定义提示词模板的字符串，其中包含文本和变量占位符（如{name}） ；
#   2、input_variables： 列表，指定了模板中使用的变量名称，在调用模板时被替换；
#   3、partial_variables：字典，用于定义模板中一些固定的变量名。这些值不需要再每次调用时被替换。
# 函数方法介绍：
#   format()：给input_variables变量赋值，并返回提示词。利用format() 进行格式化时就一定要赋值，否则会报错。当在template中未设置input_variables，则会自动忽略。


# 方式1：使用构造方法实例化提示词模板
from langchain_core.prompts import PromptTemplate

print("================== 方式1：PromptTemplate =========")

# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 该模板包含两个变量：role（角色）和question（问题）
# partial_variables 设置默认值
template = PromptTemplate(
    template="你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}",
    input_variables=["role", "question"],
    partial_variables={"role": "AI开发"},
)

# 使用模板格式化具体的提示词内容
# 将role替换为"python开发"，question替换为"冒泡排序怎么写？"
prompt1 = template.format(question="冒泡排序怎么写,只要代码其它不要，简洁")
prompt2 = template.format(
    role="python开发", question="冒泡排序怎么写,只要代码其它不要，简洁"
)
# 输出格式化后的提示词内容
print(prompt1)
print(prompt2)
# 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写,只要代码其它不要，简洁


# 方式2：使用 from_template 方法实例化提示词模板
from langchain_core.prompts import PromptTemplate

print("================== 方法 2 PromptTemplate.from_template =========")

# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 模板包含两个占位符：{role}表示角色，{question}表示问题
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)

# 使用指定的角色和问题参数来格式化模板，生成最终的提示词字符串
prompt = template.format(role="python开发", question="快速排序怎么写？")

# 输出生成的提示词
print(prompt)

print("\n\n")

print("================== invoke 创建模版  =========")


"""
invoke() 是 LangChain Expression Language（LCEL 的统一执行入口，用于执行任意可运行对象（Runnable ）。返回的是一个 PromptValue 对象，
可以用 .to_string() 或 .to_messages() 查看内容
"""
from langchain_core.prompts import PromptTemplate

# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 模板中包含两个占位符：{role}表示角色，{question}表示问题
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)

# 使用invoke方法填充模板中的占位符，生成具体的提示词
# 参数：字典类型，包含role和question两个键值对
# 返回值：PromptValue对象，包含了格式化后的提示词
prompt = template.invoke({"role": "python开发", "question": "冒泡排序怎么写？"})

# 打印PromptValue对象及其类型
print(prompt)
print(type(prompt))
print()

# 将PromptValue对象转换为字符串并打印
# to_string()方法将PromptValue转换为可读的字符串格式
print(prompt.to_string())
print(type(prompt.to_string()))
print()

print(prompt.to_messages())
print(type(prompt.to_messages()))
