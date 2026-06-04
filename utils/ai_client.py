# AI客户端封装，负责与DeepSeek API交互

import os
from openai import OpenAI
from .constants import DEFAULT_BASE_URL, DEFAULT_MODEL

class AIClient:
    def __init__(self, api_key=None, base_url=None):
        # 从环境变量或参数获取API_KEY
        self.api_key = api_key or os.environ.get('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("请设置环境变量 DEEPSEEK_API_KEY 或在代码中传入 api_key")
        self.base_url = base_url or DEFAULT_BASE_URL
        self.model = DEFAULT_MODEL
        # 创建与AI大模型交互的客户端对象
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def stream_chat(self, system_prompt, messages):
        """流式对话，返回生成器，每次yield一个内容片段"""
        # 调用AI大模型，并且交互
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages  # 保存的聊天记录(解决会话记忆)
            ],
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content