from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All config comes from env vars (or .env). Bad values fail at import, not mid-request."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://docintel:docintel@localhost:5432/docintel"
    redis_url: str = "redis://localhost:6379/0"
    upload_dir: str = "/tmp/docintel-uploads"

    # Auth
    jwt_secret: str = Field(min_length=32)  # required; no default so a forgotten secret fails at startup
    jwt_expire_minutes: int = 60 * 8

    # Upload limits
    max_upload_mb: float = 10.0
    max_pages: int = 50
    max_files_per_request: int = 20

    # LLM: any OpenAI-compatible /chat/completions endpoint (Ollama, Groq, OpenAI, vLLM...)
    llm_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "qwen2.5:1.5b"
    llm_api_key: str = "ollama"
    llm_timeout_s: float = 120.0
    llm_enabled: bool = True
    llm_max_chars: int = 12000  # per chunk sent to the model

    # Worker
    task_max_retries: int = 3
    task_soft_time_limit_s: int = 300
    stale_processing_s: int = 600  # a 'processing' row older than this is treated as a crashed worker
    celery_eager: bool = False  # run tasks inline (tests / no-Redis dev)

    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
