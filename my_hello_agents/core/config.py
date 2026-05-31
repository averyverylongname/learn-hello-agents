import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class LLMConfig:
    model: str = os.getenv("LLM_MODEL", "deepseek-v4-pro")
    api_key: str = os.getenv("LLM_API_KEY", "")
    base_url: str = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
    temperature: float = 0.7
    max_tokens: int = 1024

    def validate(self):
        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置，请在 .env 文件中设置。")
        if not self.base_url:
            raise ValueError("LLM_BASE_URL 未配置，请在 .env 文件中设置。")
        if not self.model:
            raise ValueError("LLM_MODEL 未配置，请在 .env 文件中设置。")