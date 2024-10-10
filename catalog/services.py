from django.core.cache import cache

from catalog.models import Category
from config import settings


def get_cached_categories():
    if settings.CACHE_ENABLED:
        cache_key = 'categories_list'
        categories = cache.get(cache_key)

        if categories is None:
            categories = Category.objects.all()
            cache.set(cache_key, categories)
    else:
        categories = Category.objects.all()

    return categories