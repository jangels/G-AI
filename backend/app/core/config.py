from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "G-AI (丐要) Protocol"
    VERSION: str = "0.9.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS设置，允许前端跨域乞讨
    BACKEND_CORS_ORIGINS: list = ["http://localhost", "http://localhost:8001", "*"]
    
    # LLM 配置（从 .env 文件读取）
    GEMINI_API_KEY: str = ""  # 必填：在 .env 文件中设置
    GEMINI_MODEL: str = "models/gemini-2.5-flash"  # 可选：或 "models/gemini-2.5-pro", "models/gemini-pro-latest"
    
    # OpenAI 配置（可选，备用）
    OPENAI_API_KEY: str = "sk-placeholder"  # 可选：如需使用 OpenAI
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # LLM 提供商选择
    LLM_PROVIDER: str = "gemini"  # "gemini" 或 "openai"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()