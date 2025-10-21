"""
Configuration module for database and API settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5000
    db_name: str = "master"
    db_user: str = "sa"
    db_password: str = ""
    db_driver: str = "pymssql"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Construct SQLAlchemy database URL."""
        return f"mssql+{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# Global settings instance
settings = Settings()
