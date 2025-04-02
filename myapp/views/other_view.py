
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.cache import cache

# 退出登录
from myapp.models import Anime


def custom_logout(request):
    # 获取当前页面路径（需通过GET参数传递）
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    logout(request)
    return redirect(next_url)



def search_view(request):
    query = request.GET.get('q', '')
    print(query)
    cache_key = f'query_{query}'
    print(cache_key)
    results = cache.get(cache_key)
    if not results:
        search_query = (
                Q(anime_name__icontains=query) |
                Q(resume__icontains=query) |
                Q(animetag__tag__tag_name__icontains=query)  # 通过标签名关联查询
        )

        results = Anime.objects.filter(search_query).distinct().order_by('-release_time')
        cache.set(cache_key,results,20)
        # print('save to cache')
    flag = False
    if results:
        flag = True


    # 分页逻辑（复用more_view逻辑）
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 生成页码范围
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start = max(current_page - 5, 1)
    end = min(current_page + 5, total_pages)
    page_range = sorted(list(set(
        [1] + list(range(start, end + 1)) + ([total_pages] if total_pages > 0 else [])
    )))


    return render(request, 'search_results.html', {
        'page_obj': page_obj,
        'custom_page_range': page_range,
        'search_query': query,
        'has_results': flag
    })

from django.shortcuts import render
from django.db.models import Count
from myapp.models import Tag, AnimeTag

def filter(request):
    # 获取热门标签（关联动漫最多的前15个）
    hot_tags = Tag.objects.annotate(
        anime_count=Count('animetag')
    ).order_by('-anime_count')[:15]

    return render(request, 'filter.html', {
        'hot_tags': hot_tags
    })


def search_tags(request):
    query = request.GET.get('q', '')
    tags = Tag.objects.filter(tag_name__icontains=query)[:10]
    results = [{'id': t.tag_id, 'name': t.tag_name} for t in tags]
    return JsonResponse({'results': results})


# 在other_view.py中添加筛选处理函数
from django.http import JsonResponse
from django.db.models import Q
from myapp.models import Anime, AnimeTag
from datetime import datetime
import calendar

from django.core.paginator import Paginator
from django.shortcuts import render


def filter_results(request):
    # 获取所有筛选参数
    tags = request.GET.getlist('tags')  # 使用GET参数传递
    all_time = request.GET.get('all_time', 'true') == 'true'
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    all_rating = request.GET.get('all_rating', 'true') == 'true'
    min_rating = float(request.GET.get('min_rating', 0))
    max_rating = float(request.GET.get('max_rating', 10))
    sort_by = request.GET.get('sort_by', 'time')

    # 构建查询条件（与之前相同）
    query = Q()
    if tags:
        for tag_id in tags:
            query &= Q(animetag__tag_id=tag_id)

    if not all_time and start_time and end_time:
        try:
            start_date = datetime.strptime(start_time, '%Y-%m').date()
            end_year_month = datetime.strptime(end_time, '%Y-%m')
            last_day = calendar.monthrange(end_year_month.year, end_year_month.month)[1]
            end_date = end_year_month.replace(day=last_day).date()
            query &= Q(release_time__date__gte=start_date) & Q(release_time__date__lte=end_date)
        except ValueError:
            pass

    if not all_rating:
        query &= Q(score__gte=min_rating) & Q(score__lte=max_rating)

    # 执行查询并排序
    animes = Anime.objects.filter(query).distinct()
    if sort_by == 'time':
        animes = animes.order_by('-release_time')
    elif sort_by == 'rating':
        animes = animes.order_by('-score')

    # 分页逻辑
    paginator = Paginator(animes, 10)  # 每页10条
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 生成页码范围（与search_view相同逻辑）
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start = max(current_page - 5, 1)
    end = min(current_page + 5, total_pages)
    page_range = sorted(list(set([1] + list(range(start, end + 1)) + ([total_pages] if total_pages > 0 else []))))

    # 构建筛选描述
    filter_description = []
    if tags:
        tag_names = Tag.objects.filter(tag_id__in=tags).values_list('tag_name', flat=True)
        filter_description.append(f"标签：{', '.join(tag_names)}")
    if not all_time and start_time and end_time:
        filter_description.append(f"时间：{start_time} 至 {end_time}")
    if not all_rating:
        filter_description.append(f"评分：{min_rating} - {max_rating}")

    return render(request, 'search_results.html', {
        'page_obj': page_obj,
        'custom_page_range': page_range,
        'has_results': page_obj.object_list.exists(),
        'search_query': " | ".join(filter_description) if filter_description else "全部作品",
        'is_filter': True  # 添加标识用于模板判断
    })
