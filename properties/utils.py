from django.core.cache import cache
import logging
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    return properties

def get_redis_cache_metrics():
    redis_client = get_redis_connection("default")
    info = redis_client.info()

    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    logger.info(f"Redis Cache Hits: {hits}")
    logger.info(f"Redis Cache Misses: {misses}")
    logger.info(f"Redis Cache Hit Ratio: {hit_ratio:.2%}")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }
