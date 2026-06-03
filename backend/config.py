from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    otx_api_key: str = ""
    database_url: str = "sqlite:///./nexus.db"
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"

settings = Settings()
