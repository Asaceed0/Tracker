import django_redis
from django.core.cache import cache
from django.http import HttpResponse


def my_view(request):
    # 尝试从缓存获取数据
    data = cache.get('my_key1')

    if not data:
        # 如果缓存中没有，生成数据并设置缓存（有效期 25秒）
        data = "This is expensive data...cache-in "
        cache.set('my_key1', data, timeout=25)
        return HttpResponse('nocache')
    return HttpResponse(data)


from django.views.decorators.cache import cache_page

@cache_page(60)  # 缓存该视图 15 分钟
def cached_view(request):
    return HttpResponse("This view is cached with Redis!")
