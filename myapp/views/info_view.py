import time

from django.shortcuts import render, HttpResponse, redirect
from myapp.functions.info_func import get_subject_content
from myapp.models import RecordAnime,Anime

from django.http import JsonResponse



def check_subscription(user_id, anime_id):
    # 查询用户和动漫对应的记录
    record = RecordAnime.objects.filter(user_id=user_id, anime_id=anime_id).first()

    if record:
        # 获取total（需通过关联的Anime模型）
        total = record.anime.total if record.anime else None
        score_dict = {'record':1,'score':record.score_user}
        step_dict = {'record':1,'step':record.step,'total':total}
    else:
        score_dict = {'record': 0, 'score': 0}
        step_dict = {'record': 0, 'step': 0, 'total': 0}
    return score_dict, step_dict


from django.db.models import Count
from myapp.models import Anime, AnimeTag


def get_similar_animes(subject_id):
    # 1. 获取目标动漫的所有标签ID
    target_tags = AnimeTag.objects.filter(anime_id=subject_id).values_list('tag_id', flat=True)

    if not target_tags:
        return []  # 若目标动漫无标签，返回空

    # 2. 筛选具有共同标签的动漫（排除自身），并按共同标签数排序
    similar_animes = (
        AnimeTag.objects
            .filter(tag_id__in=target_tags)
            .exclude(anime_id=subject_id)  # 排除目标动漫自身
            .values('anime_id')  # 按动漫ID分组
            .annotate(common_tags=Count('tag_id'))  # 统计共同标签数
            .order_by('-common_tags')[:7]  # 按共同标签数降序，取前7
    )

    # 3. 提取动漫ID列表
    similar_anime_ids = [item['anime_id'] for item in similar_animes]

    # 4. 查询这些动漫的完整信息
    results = Anime.objects.filter(anime_id__in=similar_anime_ids)

    # 5. 序列化为字典（包含所有字段）
    reco_7 = [
        {
            'anime_id': anime.anime_id,
            'anime_name': anime.anime_name,
            'info_url': anime.info_url,
            'score': anime.score,
            'img_url': anime.img_url,
            'total': anime.total,
            'resume': anime.resume,
            'release_time': anime.release_time
        }
        for anime in results
    ]

    return reco_7


def subject_info(request, subject_id):
    # print(subject_id)
    response_data = get_subject_content(subject_id)
    if response_data['success']:
        data = response_data['data']

        s = time.time()
        data['user_score'],data['step'] = check_subscription(request.user.id,subject_id)
        rec_7 = get_similar_animes(subject_id)
        e = time.time()
        print(f'======查询耗时{e -s}')

        return render(request,'subject_info.html',{'data':data,'rec_7':rec_7})

    # 暂定
    return HttpResponse(f'加载失败了,code:{response_data["code"]}')
