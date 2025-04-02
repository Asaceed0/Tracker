# categories_view.py
from django.shortcuts import render
from django.core.paginator import Paginator
from myapp.models import Anime, AnimeTag,Tag


def categories(request, tag_id):
    # 获取排序方式参数，默认按时间排序

    try:
        current_tag = Tag.objects.get(tag_id=tag_id)
        tag_name = current_tag.tag_name
    except Tag.DoesNotExist:
        tag_name = "未知标签"
    sortway = request.GET.get('sortway', '0')

    # 根据tag_id获取关联的动漫
    anime_ids = AnimeTag.objects.filter(tag_id=tag_id).values_list('anime_id', flat=True)
    anime_list = Anime.objects.filter(anime_id__in=anime_ids)

    # 设置排序方式
    if sortway == 'M':
        anime_list = anime_list.order_by('-score')  # 按评分降序
    else:
        anime_list = anime_list.order_by('-release_time')  # 按时间降序

    # 分页处理
    paginator = Paginator(anime_list, 10)  # 每页10条
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 自定义页码范围（与more_view逻辑一致）
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start = max(current_page - 5, 1)
    end = min(current_page + 5, total_pages)
    page_range = sorted(list(set(
        [1] +
        list(range(start, end + 1)) +
        ([total_pages] if total_pages > 0 else [])
    )))

    return render(request, 'categories.html', {
        'page_obj': page_obj,
        'custom_page_range': page_range,
        'current_sort': sortway,
        'tag_id': tag_id,
        'tag_name':tag_name
    })