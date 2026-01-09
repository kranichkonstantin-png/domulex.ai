"""
Configuration management for DOMULEX Backend
"""

from functools import lru_cache
from typing import List

from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file='.env',
        case_sensitive=False,
        extra='ignore',  # Ignore extra fields
    )
    
    # Gemini API
    gemini_api_key: str
    
    # Qdrant Vector DB
    qdrant_url: str = ""  # Full URL for Qdrant Cloud (takes precedence)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "legal_documents"
    qdrant_use_https: bool = False
    qdrant_api_key: str = ""  # API Key for Qdrant Cloud
    
    # CORS - parsed from comma-separated string
    cors_origins: str = "http://localhost:3000,https://domulex-ai.web.app,https://domulex.ai,https://www.domulex.ai"
    
    def get_cors_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(',')]
    
    # Firebase (optional - for authentication)
    firebase_project_id: str = ""
    firebase_private_key_id: str = ""
    firebase_private_key: str = ""
    firebase_client_email: str = ""
    
    # Redis (optional - for caching)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    enable_cache: bool = False
    cache_ttl: int = 3600
    
    # Stripe (for payments)
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_tenant: str = ""
    stripe_price_pro: str = ""
    stripe_price_lawyer: str = ""
    
    # Celery (Task Queue)
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    # API Keys
    courtlistener_api_key: str = ""
    
    # Monitoring
    sentry_dsn: str = ""
    sentry_environment: str = "development"
    log_level: str = "INFO"
    
    # Feature Flags
    enable_pdf_analysis: bool = True
    enable_conflict_resolution: bool = True
    enable_auto_ingestion: bool = False
    
    # API Settings
    api_title: str = "DOMULEX Backend"
    api_version: str = "0.1.0"
    
    # Environment
    environment: str = "development"
    debug: bool = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
