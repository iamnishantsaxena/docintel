from pydantic import Field, model_validator
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
    llm_base_url: str = "http://localhost:11434/v1"  # empty = no local model (cloud-only deployments)
    llm_model: str = "qwen2.5:1.5b"
    llm_api_key: str = "ollama"
    llm_timeout_s: float = 120.0
    llm_enabled: bool = True
    llm_max_chars: int = 12000  # per chunk sent to the model
    llm_max_tokens: int = 2048  # cap on the reply; a runaway reply truncates → bad JSON → regex fallback

    # Optional cloud model, tried before the local one only when its API key is set. Opt-in because the
    # document text is sent to that provider. Any failure there falls back to the local model above.
    cloud_llm_base_url: str = ""
    cloud_llm_model: str = ""
    cloud_llm_api_key: str = ""

    # Worker
    task_max_retries: int = 3
    task_soft_time_limit_s: int = 300
    stale_processing_s: int = 600  # a 'processing' row older than this is treated as a crashed worker
    celery_eager: bool = False  # run tasks inline (tests / no-Redis dev)

    cors_origins: list[str] = ["http://localhost:5173"]

    @model_validator(mode="after")
    def _cloud_complete(self):
        if self.cloud_llm_api_key and not (self.cloud_llm_base_url and self.cloud_llm_model):
            raise ValueError("CLOUD_LLM_API_KEY is set but CLOUD_LLM_BASE_URL or CLOUD_LLM_MODEL is missing")
        return self

    def llm_endpoints(self) -> list[tuple[str, str, str]]:
        """(base_url, model, api_key) in the order they're tried: cloud (if keyed), then local (if set)."""
        eps = [(self.cloud_llm_base_url, self.cloud_llm_model, self.cloud_llm_api_key)] if self.cloud_llm_api_key else []
        return eps + ([(self.llm_base_url, self.llm_model, self.llm_api_key)] if self.llm_base_url else [])


settings = Settings()
