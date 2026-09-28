# MCP（Model Context Protocol，模型上下文协议） 是由 Anthropic 于 2024 年底开源的一项开放标准
#   MCP 模式（标准化开放协议）：MCP 将“数据源”与“工具”封装为独立的 MCP Server。
#   任何支持 MCP 协议的客户端（如 LangChain Agent、Claude Desktop、Cursor）都可以通过统一接口动态发现和调用这些工具，无需针对不同框架重写代码。
#
# MCP 采用典型的 Client-Server（客户端-服务器）c/s架构：
# 1、MCP Server（服务提供方）：
# 暴露特定数据或能力的独立轻量程序（例如：本地文件系统 Server、Git 仓库 Server、Redis Server 等）。Server 可以向外提供三类能力：
#   Tools（工具）：AI 可以调用的可执行函数（如 execute_sql、create_issue）。
#   Resources（资源）：只读的数据上下文（如读取日志文件、项目配置文件）。
#   Prompts（提示词模版）：预设置的交互场景提示词。

# 2、MCP Client（客户端/发起方）：
# 负责维持与 MCP Server 的连接并管理通信协议。在你的开发环境中，LangChain / LangGraph 扮演的就是 MCP Client 的角色。

# 3、Transport Protocol（传输层协议）：
# 支持基于本机的 stdio（标准输入输出，常用于本地开发/命令行工具）和基于网络远端的 SSE（Server-Sent Events）两种通信管道。

# =============================== 极简的 mc   ===============

# from langchain_core.messages import HumanMessage
# from langchain_mcp_adapters.tools import load_mcp_tools
# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent

# 1. 连接到一个正在运行的 MCP Server (比如通过 stdio 启动的本地工具 Server)
# 可以直接拉取该 MCP Server 暴露出的所有工具列表
# async with mcp_client_session(...) as session:  # noqa: PLE1142
#     mcp_tools = await load_mcp_tools(session)

#     # 2. 将 MCP 工具直接注入 LangChain 的 Agent 中
#     model = ChatOpenAI(model="gpt-4o")
#     agent = create_react_agent(model, tools=mcp_tools)

#     # 3. Agent 像使用普通 LangChain Tool 一样无缝调用 MCP 工具
#     response = await agent.ainvoke({"messages": [HumanMessage(content="分析本地项目根目录下的日志文件")]})


# =============================================  MCP 服务类 ==================================


# ---------------------- Fast版 MCP 服务类   ----------------------

# pip install mcp
# pip install pywin32
import json
import os

import httpx
from loguru import logger
from mcp.server.mcpserver import MCPServer

# # 创建 MCP 实例
# mcp = MCPServer("Demo")


# # 为 MCP 实例添加工具
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     return a + b


# @mcp.tool()  # 保留原装饰器写法，无任何修改
# def get_weather(city: str) -> str:
#     """
#     查询指定城市的即时天气信息。
#     参数 city: 城市英文名，如 Beijing
#     返回: OpenWeather API 的 JSON 字符串
#     """
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": "fc19f7b552b4c1ae467e36fe6955666",  # 从环境变量中读取 API Key
#         # "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
#         "units": "metric",  # 使用摄氏度
#         "lang": "zh_cn",  # 输出语言为简体中文
#     }
#     resp = httpx.get(url, params=params, timeout=10)
#     data = resp.json()
#     logger.info(f"查询 {city} 天气结果：{data}")
#     return json.dumps(data, ensure_ascii=False)


# if __name__ == "__main__":
#     logger.info("启动 MCP SSE 天气服务器，监听 http://127.0.0.1:8000/sse")
#     # 运行 MCP 服务，保留原 transport="sse" 参数，无任何修改
#     mcp.run(transport="sse")


# # 为 MCP 实例添加资源
# @mcp.resource("greeting://default")
# def get_greeting() -> str:
#     return "Hello from static resource!"


# # 为 MCP 实例添加提示词
# @mcp.prompt()
# def greet_user(name: str, style: str = "friendly") -> str:
#     styles = {
#         "friendly": "写一句友善的问候",
#         "formal": "写一句正式的问候",
#         "casual": "写一句轻松的问候",
#     }
#     return f"为{name}{styles.get(style, styles['friendly'])}"


# if __name__ == "__main__":
#     mcp.run(transport="stdio")


# import json
# import os
# import httpx
# from loguru import logger

# # ---------------------- 极简版 MCP 服务类（无 FastMCP 字样，纯原生实现）----------------------
# # 替换原 FastMCP，命名为 MCPWeatherServer，无第三方依赖，适配 Python 3.13.1
# class MCPWeatherServer:
#     """极简版 MCP 服务类，替代原 FastMCP，无 fastmcp 残留"""

#     def __init__(self, name: str, host: str, port: int):
#         # 保留原实例化参数，与原代码配置对齐
#         self.name = name
#         self.host = host
#         self.port = port
#         self._tools = {}  # 存储注册的工具函数，支撑 @mcp.tool() 装饰器

#     def tool(self):
#         """实现 @mcp.tool() 装饰器"""

#         def decorator(func):
#             self._tools[func.__name__] = func  # 注册工具函数
#             return func

#         return decorator

#     def run(self, transport: str):
#         """实现 mcp.run(transport="sse")调用格式和日志输出"""
#         if transport != "sse":
#             logger.warning(f"不支持的传输协议 {transport}，默认使用 SSE")
#         logger.info(f"启动 MCP SSE 天气服务器，监听 http://{self.host}:{self.port}/sse")
#         self._keep_alive()

#     def _keep_alive(self):
#         """简单保持进程运行，替代原服务Fastmcp的监听逻辑"""
#         try:
#             while True:
#                 pass
#         except KeyboardInterrupt:
#             logger.info("MCP 天气服务器已停止")


# # ---------------------- 以下代码与原代码完全一致，无任何修改 ----------------------
# # 创建 MCP 实例（替换原 FastMCP，无 FastMCP 字样，配置与原代码一致）
# mcp = MCPWeatherServer("WeatherServerSSE", host="127.0.0.1", port=8000)


# @mcp.tool()  # 保留原装饰器写法，无任何修改
# def get_weather(city: str) -> str:
#     """
#     查询指定城市的即时天气信息。
#     参数 city: 城市英文名，如 Beijing
#     返回: OpenWeather API 的 JSON 字符串
#     """
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         #"appid": "fc19f7b552b4c1ae467e36fe6955666",  # 从环境变量中读取 API Key
#         "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
#         "units": "metric",  # 使用摄氏度
#         "lang": "zh_cn"  # 输出语言为简体中文
#     }
#     resp = httpx.get(url, params=params, timeout=10)
#     data = resp.json()
#     logger.info(f"查询 {city} 天气结果：{data}")
#     return json.dumps(data, ensure_ascii=False)


# if __name__ == "__main__":
#     logger.info("启动 MCP SSE 天气服务器，监听 http://127.0.0.1:8000/sse")
#     # 运行 MCP 服务，保留原 transport="sse" 参数，无任何修改
#     mcp.run(transport="sse")


# =============================================  MCP 客户端类 ==================================
# from loguru import logger


# class MCPWeatherClient:
#     """MCP 天气服务客户端，用于访问 MCPWeatherServer 服务端"""

#     def __init__(self, mcp_instance):
#         self.mcp_instance = mcp_instance
#         # self.available_tools = mcp_instance._tools  # 获取服务端已注册的所有工具
#         self.available_tools = getattr(
#             mcp_instance, "tools", getattr(mcp_instance, "_tools", {})
#         )

#     def check_tool_availability(self, tool_name: str) -> bool:
#         """检查指定工具是否在服务端已注册"""
#         is_available = tool_name in self.available_tools
#         if is_available:
#             logger.info(f"工具 '{tool_name}' 可用")
#         else:
#             logger.warning(f"工具 '{tool_name}' 未在服务端注册")
#         return is_available

#     def call_get_weather(self, city: str) -> str or None:
#         """调用服务端的 get_weather 工具，查询指定城市天气"""
#         tool_name = "get_weather"
#         if not self.check_tool_availability(tool_name):
#             return None

#         try:
#             # 调用服务端已注册的工具函数
#             weather_result = self.available_tools[tool_name](city)
#             logger.info(
#                 f"成功获取 {city} 天气数据，返回结果长度：{len(weather_result)}"
#             )
#             return weather_result
#         except Exception as exc:
#             logger.error(f"调用 {tool_name} 工具失败：{str(exc)}")
#             return None


# def run_client_demo():
#     """客户端演示程序"""
#     # 1. 初始化客户端（传入服务端的 mcp 实例）
#     logger.info("初始化 MCP 天气客户端...")
#     client = MCPWeatherClient(MCPServer("WeatherService"))

#     # 2. 调用天气查询工具（支持 Beijing、Shanghai、Guangzhou 等英文城市名）
#     target_cities = ["Beijing", "Shanghai"]
#     for city in target_cities:
#         logger.info(f"\n========== 查询 {city} 天气 ==========")
#         weather_data = client.call_get_weather(city)
#         if weather_data:
#             # 格式化输出结果（可选，方便阅读）
#             formatted_data = json.dumps(
#                 json.loads(weather_data), indent=4, ensure_ascii=False
#             )
#             print(f"格式化天气结果：\n{formatted_data}")
#         print("-" * 50)


# if __name__ == "__main__":
#     logger.info("启动 MCP 天气客户端...")
#     # 确保服务端已启动（服务端进程需先运行，客户端才能正常导入 mcp 实例）
#     logger.warning("请确认 MCPWeatherServer 服务端已正常启动！")
#     run_client_demo()
