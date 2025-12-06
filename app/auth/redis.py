try:
    import aioredis
    REDIS_AVAILABLE = True
except (ImportError, TypeError):
    # aioredis has compatibility issues with Python 3.12
    # Fall back to in-memory blacklist for development
    REDIS_AVAILABLE = False

from app.core.config import get_settings

settings = get_settings()

# In-memory blacklist for when Redis is not available
_in_memory_blacklist = set()

async def get_redis():
    if REDIS_AVAILABLE:
        if not hasattr(get_redis, "redis"):
            try:
                get_redis.redis = await aioredis.from_url(
                    settings.REDIS_URL or "redis://localhost"
                )
            except Exception:
                # Fall back to in-memory if Redis connection fails
                return None
        return get_redis.redis
    return None

async def add_to_blacklist(jti: str, exp: int):
    if REDIS_AVAILABLE:
        try:
            redis = await get_redis()
            if redis:
                await redis.set(f"blacklist:{jti}", "1", ex=exp)
                return
        except Exception:
            pass
    # Fall back to in-memory storage
    _in_memory_blacklist.add(jti)

async def is_blacklisted(jti: str) -> bool:
    if REDIS_AVAILABLE:
        try:
            redis = await get_redis()
            if redis:
                return await redis.exists(f"blacklist:{jti}")
        except Exception:
            pass
    # Fall back to in-memory check
    return jti in _in_memory_blacklist