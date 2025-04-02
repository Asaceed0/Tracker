
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
from myapp.models import Tag, AnimeTag


def tag_collect(request):
    # 获取标签并按关联动漫数降序排序
    tag_list = Tag.objects.annotate(
        anime_count=Count('animetag')
    ).order_by('-anime_count')

    # 分页处理（每页20个）
    paginator = Paginator(tag_list, 20)
    page_number = request.GET.get('page', 1)
    tags = paginator.get_page(page_number)

    # 生成自定义页码范围（仿more视图逻辑）
    current_page = tags.number
    total_pages = tags.paginator.num_pages
    start = max(current_page - 3, 1)
    end = min(current_page + 3, total_pages)

    page_range = list(range(start, end + 1))
    if 1 not in page_range:
        page_range.insert(0, 1)
    if total_pages not in page_range and total_pages > 0:
        page_range.append(total_pages)
    page_range = sorted(list(set(page_range)))

    return render(request, 'tags.html', {
        'tags': tags,
        'custom_page_range': page_range
    })