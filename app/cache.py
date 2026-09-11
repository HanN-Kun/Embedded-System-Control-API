import json
import time
import redis

from app.config import settings

_redis_client = redis.from_url(settings.redis_url, decode_responses=True)

_local_cache: dict[str, tuple[float, str]] = {}


def _local_get(key: str) -> str | None:
    entry = _local_cache.get(key)
    if entry is None:
        return None
    expires_at, value = entry
    if time.time() > expires_at:
        del _local_cache[key]
        return None
    return value


def _local_set(key: str, value: str, ttl: int) -> None:
    _local_cache[key] = (time.time() + ttl, value)


def _local_delete(key: str) -> None:
    _local_cache.pop(key, None)


def cache_get(key: str) -> dict | list | None:
    local_value = _local_get(key)
    if local_value is not None:
        return json.loads(local_value)

    redis_value = _redis_client.get(key)
    if redis_value is not None:
        _local_set(key, redis_value, ttl=60)
        return json.loads(redis_value)

    return None


def cache_set(key: str, value: dict | list, ttl: int = 300) -> None:
    serialized = json.dumps(value)
    _local_set(key, serialized, ttl=min(ttl, 60))
    _redis_client.set(key, serialized, ex=ttl)


def cache_delete(key: str) -> None:
    _local_delete(key)
    _redis_client.delete(key)