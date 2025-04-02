from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
from myapp.functions.home_func import get_user_anime_records, get_user_details, get_user_records
from django.core.paginator import Paginator

from django.db.models import Count
from myapp.models import RecordAnime, AnimeTag, Tag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone  # ⭐️ 新增导入


# def more(request):
#     items_anime = get_user_anime_records(request.user.id)
#     # print(items_anime)
#
#     recently_record = get_user_records(request.user.id)
#     print(recently_record)
#
#     return render(request, template_name='more.html',
#                   context={'items_anime': items_anime[:3],
#                            'recently_record': recently_record})


# def more(request):
#     anime_list =  get_user_anime_records(request.user.id)
#     paginator_anime = Paginator(anime_list, 5)  # 每页10条
#     page_number = request.GET.get('page')
#     items_anime = paginator_anime.get_page(page_number)
#
#     return render(request, 'more.html', {
#         'items_anime': items_anime,
#
#     })


def get_tag_stats(request):
    print('=============================')
    user_animes = RecordAnime.objects.filter(user=request.user).values_list('anime', flat=True)

    tags_data = (
        Tag.objects
            .filter(animetag__anime__in=user_animes)
            .annotate(count=Count('animetag'))
            .order_by('-count')[:7]
    )

    chart_data = [
        {"name": tag.tag_name, "value": tag.count}
        for tag in tags_data
    ]
    return JsonResponse({"chart_data": chart_data})  # 返回标准JSON




def more(request):
    print('=================================', request.user.id)
    anime_list = get_user_anime_records(request.user.id)
    paginator_anime = Paginator(anime_list, 5)
    page_number = request.GET.get('page', 1)
    items_anime = paginator_anime.get_page(page_number)

    # 自定义页码范围计算
    current_page = items_anime.number
    total_pages = items_anime.paginator.num_pages

    # 当前页前后扩展5页
    start = max(current_page - 5, 1)
    end = min(current_page + 5, total_pages)

    # 生成页码范围并确保包含首尾页
    page_range = list(range(start, end + 1))
    if 1 not in page_range:
        page_range.insert(0, 1)
    if total_pages not in page_range and total_pages > 0:
        page_range.append(total_pages)

    # 去重并排序
    page_range = sorted(list(set(page_range)))

    return render(request, 'more.html', {
        'items_anime': items_anime,
        'custom_page_range': page_range  # 新增自定义页码范围
    })


@csrf_exempt
@require_POST
def delete_record(request):
    print('调用了删除记录的api')
    # 验证登录状态
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'msg': '请先登录'}, status=403)

    # 获取记录ID
    record_id = request.POST.get('record_id')
    if not record_id:
        return JsonResponse({'status': 'error', 'msg': '参数错误'}, status=400)

    try:
        # 查询并删除记录（验证用户所有权）
        record = RecordAnime.objects.get(record_id=record_id, user=request.user)
        record.delete()
        return JsonResponse({'status': 'success'})
    except RecordAnime.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': '记录不存在'}, status=404)

        # from django.http import JsonResponse
        #
        #
        # def delete_record(request):
        #     if request.method == "POST":
        #         record_id = request.POST.get('record_id')
        #         try:
        #             record = RecordAnime.objects.get(record_id=record_id)
        #             record.delete()
        #             return JsonResponse({'status': 'success', 'msg': '删除成功'})
        #         except RecordAnime.DoesNotExist:
        #             return JsonResponse({'status': 'error', 'msg': '记录不存在'})
        #
        #



@csrf_exempt
@require_POST
def resubscribe(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'msg': '请先登录'}, status=403)

    try:
        data = json.loads(request.body)
        # 创建新记录

        # 在视图函数内部修改：
        new_record = RecordAnime.objects.create(
            user=request.user,
            anime_id=data['anime_id'],
            step=data.get('step', 0),
            score_user=data.get('score_user', 0),
            time=timezone.now()  # ⭐️ 自动填充当前时间
        )
        return JsonResponse({
            'status': 'success',
            'record_id': new_record.record_id
        })
    except KeyError as e:
        return JsonResponse({'status': 'error', 'msg': f'缺少必要参数: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)


@csrf_exempt
@require_POST
def update_step(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'msg': '请先登录'}, status=403)

    try:
        data = json.loads(request.body)
        record = RecordAnime.objects.get(
            record_id=data['record_id'],
            user=request.user  # 验证记录属于当前用户
        )
        record.step = data['new_step']
        record.save()
        return JsonResponse({'status': 'success'})
    except RecordAnime.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': '记录不存在'}, status=404)
    except KeyError as e:
        return JsonResponse({'status': 'error', 'msg': f'参数错误: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)



@csrf_exempt
@require_POST
def update_rating(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'msg': '请先登录'}, status=403)

    try:
        data = json.loads(request.body)
        record = RecordAnime.objects.get(
            record_id=data['record_id'],
            user=request.user
        )
        new_rating = float(data['new_rating'])
        if not (0 <= new_rating <= 10):
            raise ValueError("评分必须在0-10之间")

        record.score_user = new_rating
        record.save()
        return JsonResponse({'status': 'success'})
    except RecordAnime.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': '记录不存在'}, status=404)
    except (KeyError, ValueError) as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)