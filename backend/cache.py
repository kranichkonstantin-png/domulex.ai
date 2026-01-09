"""
Redis Caching Layer for DOMULEX
"""

import json
import logging
import hashlib
from typing import Optional, Any
from functools import wraps

import redis
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Redis client (initialized lazily)
_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """Get Redis client if caching is enabled."""
    global _redis_client
    
    if not settings.enable_cache:
        return None
    
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            # Test connection
            _redis_client.ping()
            logger.info("✅ Redis cache connected")
        except Exception as e:
            logger.warning(f"⚠️ Redis cache unavailable: {e}")
            _redis_client = None
    
    return _redis_client


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate deterministic cache key from arguments."""
    # Combine all arguments into a string
    key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
    # Hash for consistent length
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    return f"domulex:{prefix}:{key_hash}"


def cache_result(prefix: str, ttl: int = 3600):
    """
    Decorator to cache function results in Redis.
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds (default 1 hour)
    
    Usage:
    ```python
    @cache_result("query", ttl=1800)
    async def query_legal_documents(query: str):
        # Expensive operation
        return result
    ```
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            client = get_redis_client()
            
            # If cache disabled or unavailable, skip caching
            if client is None:
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key = generate_cache_key(prefix, *args, **kwargs)
            
            try:
                # Try to get from cache
                cached = client.get(cache_key)
                if cached:
                    logger.debug(f"📦 Cache HIT: {cache_key}")
                    return json.loads(cached)
                
                # Cache miss - execute function
                logger.debug(f"❌ Cache MISS: {cache_key}")
                result = await func(*args, **kwargs)
                
                # Store in cache
                client.setex(
                    cache_key,
                    ttl,
                    json.dumps(result, default=str)  # default=str for datetime
                )
                
                return result
            
            except Exception as e:
                logger.warning(f"Cache error: {e}")
                # Fallback to function execution
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def cache_embedding(embedding: list[float], text: str, ttl: int = 86400):
    """
    Cache embedding vector for text.
    Reduces redundant API calls to Gemini.
    
    Args:
        embedding: Vector embedding
        text: Original text
        ttl: Time to live (default 24 hours)
    """
    client = get_redis_client()
    if client is None:
        return
    
    try:
        text_hash = hashlib.md5(text.encode()).hexdigest()
        key = f"domulex:embedding:{text_hash}"
        client.setex(key, ttl, json.dumps(embedding))
    except Exception as e:
        logger.warning(f"Failed to cache embedding: {e}")


def get_cached_embedding(text: str) -> Optional[list[float]]:
    """
    Retrieve cached embedding for text.
    
    Args:
        text: Text to look up
        
    Returns:
        Cached embedding vector or None
    """
    client = get_redis_client()
    if client is None:
        return None
    
    try:
        text_hash = hashlib.md5(text.encode()).hexdigest()
        key = f"domulex:embedding:{text_hash}"
        cached = client.get(key)
        
        if cached:
            logger.debug(f"📦 Embedding cache HIT")
            return json.loads(cached)
        
        return None
    except Exception as e:
        logger.warning(f"Failed to get cached embedding: {e}")
        return None


def invalidate_cache_pattern(pattern: str):
    """
    Invalidate all cache keys matching pattern.
    
    Args:
        pattern: Redis key pattern (e.g., "domulex:query:*")
    """
    client = get_redis_client()
    if client is None:
        return
    
    try:
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
            logger.info(f"🗑️ Invalidated {len(keys)} cache keys: {pattern}")
    except Exception as e:
        logger.warning(f"Failed to invalidate cache: {e}")


def clear_all_cache():
    """Clear all DOMULEX cache."""
    invalidate_cache_pattern("domulex:*")
