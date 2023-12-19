from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"
    chroma_host: str = "localhost"
    chroma_port: str = "8080"
    cvpartner_token: str = Field(
        alias="CVPARTNER_TOKEN", description="Token for the CV Partner API."
    )
    cvhelper_host: str = "localhost"
    cvhelper_port: str = "3000"


settings = Settings()
