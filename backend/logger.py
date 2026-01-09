"""
Logging Configuration for DOMULEX
"""

import logging
import sys
from typing import Any
from datetime import datetime

try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

from config import get_settings

settings = get_settings()


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging():
    """Configure logging for the application."""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    if settings.environment == "development":
        # Colored formatter for development
        formatter = ColoredFormatter(
            '%(levelname)s | %(asctime)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # JSON formatter for production (easier to parse)
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for errors
    error_handler = logging.FileHandler('errors.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    ))
    root_logger.addHandler(error_handler)
    
    # Sentry integration (if configured)
    if SENTRY_AVAILABLE and settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.environment,
            integrations=[
                FastApiIntegration(),
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=logging.ERROR
                ),
            ],
            traces_sample_rate=1.0 if settings.environment == "development" else 0.1,
            profiles_sample_rate=1.0 if settings.environment == "development" else 0.1,
        )
        root_logger.info("✅ Sentry monitoring initialized")
    
    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    root_logger.info(f"🚀 Logging configured (level: {settings.log_level})")


class RequestLogger:
    """Middleware to log API requests."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    async def __call__(self, request, call_next):
        start_time = datetime.now()
        
        # Log request
        self.logger.info(
            f"📥 {request.method} {request.url.path} from {request.client.host}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        duration = (datetime.now() - start_time).total_seconds()
        self.logger.info(
            f"📤 {request.method} {request.url.path} → {response.status_code} ({duration:.2f}s)"
        )
        
        return response


def log_exception(exc: Exception, context: str = ""):
    """Log exception with context."""
    logger = logging.getLogger(__name__)
    
    error_msg = f"❌ Exception in {context}: {exc.__class__.__name__}: {str(exc)}"
    logger.error(error_msg, exc_info=True)
    
    # Send to Sentry if available
    if SENTRY_AVAILABLE and settings.sentry_dsn:
        sentry_sdk.capture_exception(exc)
