from pathlib import Path

from langchain_core.prompts import load_prompt

# 方式1：外部加载Prompt,将 prompt 保存为 JSON
prompt_path = Path(__file__).resolve().parent / "prompt.json"
template = load_prompt(prompt_path, encoding="utf-8")
print(template.format(name="张三", what="搞笑的"))
# 请张三讲一个搞笑的的故事


# 方式2：外部加载Prompt,将 prompt 保存为 yaml
prompt_path = Path(__file__).resolve().parent / "prompt.yaml"
template = load_prompt(str(prompt_path), encoding="utf-8")
print(template.format(name="年轻人", what="滑稽"))
# 请年轻人讲一个滑稽的故事
