from functools import lru_cache

import oeauth
import redis
from dogpile.cache.region import make_region
from gevent.queue import LifoQueue
from oe_geoutils import cache as geo_cache
from redis.connection import BlockingConnectionPool

from inventaris.constants import SETTINGS

http_requests_region_short = make_region()
http_requests_region = make_region()

system_user_cache = make_region()
regular_user_cache = make_region()


@lru_cache
def get_connectionpool(redis_url=None, max_connections=None):
    connection_pool = BlockingConnectionPool.from_url(
        redis_url,
        queue_class=LifoQueue,
        max_connections=max_connections,
    )
    return connection_pool


def add_redis_connectionpools_to_settings(settings=None):
    # Update settings with the pool references
    settings_mappings = {
        "redis.default.url": ["oeauth.cache.arguments.connection_pool"],
        "redis.cache.url": [
            "cache.inventaris.skos.arguments.connection_pool",
            "http_calls.cache.arguments.connection_pool",
            "regular_user_cache.cache.arguments.connection_pool",
            "system_user_cache.cache.arguments.connection_pool",
            "crabpy.adressenregister.cache_config.permanent.arguments.connection_pool",
            "crabpy.adressenregister.cache_config.long.arguments.connection_pool",
            "crabpy.adressenregister.cache_config.short.arguments.connection_pool",
        ],
    }
    for redis_url_key, connection_pool_keys in settings_mappings.items():
        for connection_pool_key in connection_pool_keys:
            settings[connection_pool_key] = get_connectionpool(
                redis_url=settings[redis_url_key], max_connections=int(settings["redis.max_connections"])
            )
    return settings


def init_caches(settings):
    settings = add_redis_connectionpools_to_settings(settings)

    oeauth.cache.configure_from_config(settings, "oeauth.cache.")
    if not http_requests_region_short.is_configured:
        http_requests_region_short.configure("dogpile.cache.memory", expiration_time=60)
    if (
        not http_requests_region.is_configured
        and "cache.inventaris.skos.backend" in settings
    ):
        http_requests_region.configure_from_config(settings, "cache.inventaris.skos.")



def _get_redis_client(redis_url=None, max_connections=None):
    if redis_url and max_connections:
        pool = get_connectionpool(redis_url=redis_url, max_connections=int(max_connections))
        return redis.Redis(connection_pool=pool)
    raise ValueError("A redis_url and max_connections must be set")

def get_app_redis_client(settings=None):
    # Return a Redis client using the application redis
    url = settings.get("redis.default.url") if settings else None
    max_con = settings.get("redis.max_connections") if settings else None
    return _get_redis_client(redis_url=url, max_connections=max_con)

def get_cache_redis_client(settings=None):
    # Return a Redis client using the vioe-cache redis
    url = settings.get("redis.cache.url") if settings else None
    max_con = settings.get("redis.max_connections") if settings else None
    return _get_redis_client(redis_url=url, max_connections=max_con)
