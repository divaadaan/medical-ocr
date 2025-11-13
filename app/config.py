"""Application configuration management."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # HuggingFace Configuration
    hf_token: str

    # Moonshot (Kimi K2) Configuration
    moonshot_api_key: str
    moonshot_api_base: str = "https://api.moonshot.cn/v1"

    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # File Upload Configuration
    max_upload_size_mb: int = 10
    allowed_extensions: List[str] = ["pdf", "png", "jpg", "jpeg"]

    # OCR Configuration
    ocr_model: str = "deepseek-ai/DeepSeek-OCR:novita"
    ocr_timeout: int = 300

    # LLM Configuration
    llm_model: str = "moonshot-v1-128k"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 4096

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
