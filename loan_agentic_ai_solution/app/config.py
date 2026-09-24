from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-6"
    api_base_url: str = "http://localhost:8000"
    decision_mode: str = "deterministic"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
