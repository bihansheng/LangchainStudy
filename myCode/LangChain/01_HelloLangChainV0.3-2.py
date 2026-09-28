"""
相对正式的写法，可以用在项目里
"""

import logging
import os

from dotenv import load_dotenv
from langchain_core.exceptions import LangChainException
from langchain_openai import ChatOpenAI

# .env文件读取
load_dotenv(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s -%(message)s"
)
logger = logging.getLogger(__name__)


def main():
    try:
        llm = init_llm_client()
        logger.info("初始化成功")

        # 调用模型
        # messages=[
        #     {"role": "system", "content": "你是一个有用的助手"},
        #     {"role": "user", "content": "你好，请介绍一下你自己"}
        #  ]
        question = "你是谁"
        response = llm.invoke(question)

        # 格式化输出
        logger.info(f"问题：{question}")
        logger.info(f"回答:{response.content}")

        print("======  以下是流式输出，另一种调用方式  =======")
        print("*" * 40)

        responseStream = llm.stream("介绍下 LangChain，300 字以内")
        for chunk in responseStream:
            print(chunk.content, end="")

    except ValueError as e:
        logger.error(f"配置错误：{e!s}")
    except LangChainException as e:
        logger.error(f"配置错误：{e!s}")
    except Exception as e:  # noqa: BLE001
        logger.error(f"配置错误：{e!s}")


def init_llm_client() -> ChatOpenAI:
    """初始化客户端，封装为函数"""
    api_key_m = os.getenv("SILICONFLOW_API_KEY")
    # 读取配置
    if not api_key_m:
        raise ValueError("环境变量 SILICONFLOW_API_KEY 未配置，请检查.env 文件")

    # 初始化LLM客户端
    llm = ChatOpenAI(
        model="deepseek-ai/DeepSeek-V3",
        api_key=api_key_m,
        base_url="https://api.siliconflow.cn/v1",
    )
    return llm


if __name__ == "__main__":
    main()
