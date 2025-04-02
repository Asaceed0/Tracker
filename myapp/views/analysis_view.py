from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import random

# 图表部分使用more的api
def analysis(request):
    rec_data = get_recommendations(request)
    # print(rec_data)
    return render(request, 'analysis.html',{"rec_data":rec_data})


from django.contrib.auth import get_user_model
from myapp.models import RecordAnime, AnimeTag, Tag, Anime

from django.db.models import Count


def get_tag_stats(request):
    print('=============================')
    user_animes = RecordAnime.objects.filter(user=request.user).values_list('anime', flat=True)

    tags_data = (
        Tag.objects
            .filter(animetag__anime__in=user_animes)
            .annotate(count=Count('animetag'))
            .order_by('-count')[:10]
    )

    chart_data = [
        {"name": tag.tag_name, "value": tag.count}
        for tag in tags_data
    ]
    return JsonResponse({"chart_data": chart_data})  # 返回标准JSON


from django.contrib.auth.decorators import login_required


@login_required
def get_recommendations(request):
    # 获取用户最喜欢的10个标签
    user_animes = RecordAnime.objects.filter(user=request.user).values_list('anime', flat=True)

    top_tags = (
        Tag.objects
            .filter(animetag__anime__in=user_animes)
            .annotate(count=Count('animetag'))
            .order_by('-count')[:10]
    )

    # 随机选取4个标签（或全部不足4时取全部）
    selected_tags = random.sample(list(top_tags), min(4, len(top_tags)))

    recommendations = []
    tag_names = []  # 新增：存储选中的标签名

    for tag in selected_tags:
        tag_names.append(tag.tag_name)  # 收集标签名

        # 获取该标签下用户未订阅的动漫
        subscribed_animes = RecordAnime.objects.filter(user=request.user).values_list('anime', flat=True)

        tag_animes = (
            Anime.objects
                .filter(animetag__tag=tag)
                .exclude(anime_id__in=subscribed_animes)
                .distinct()
        )

        # 随机选取最多7个
        recommended = list(tag_animes.order_by('?')[:6].values(
            'anime_id', 'anime_name', 'img_url', 'info_url'
        ))

        if recommended:
            data = {}
            data['tag_name'] = tag.tag_name
            data['animes'] = recommended
            recommendations.append(data)

    return recommendations



def get_trend_stats(request):
    # 获取用户最近30条记录

    recent_records = RecordAnime.objects.filter(user=request.user).order_by('-time')[:30]
    anime_ids = [r.anime_id for r in recent_records]

    # 统计标签
    tags = Tag.objects.filter(
        animetag__anime__in=anime_ids
    ).annotate(count=Count('animetag')).order_by('-count')[:5]

    labels = [tag.tag_name for tag in tags]
    values = [tag.count for tag in tags]
    data = {
        'labels': labels,
        'values': values
    }
    print(data)
    return JsonResponse(data)