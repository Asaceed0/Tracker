from django.forms.models import model_to_dict
from myapp.models import RecordAnime, UserInfo
from django.contrib.auth.models import User


def get_user_anime_records(user_id):
    """
    获取用户的订阅记录，预取关联的Anime数据，并按时间降序排列
    :param user_id:
    :return:
    """
    records = RecordAnime.objects.select_related('anime') \
        .filter(user_id=user_id) \
        .order_by('-time')

    result = []
    for record in records:
        record_dict = model_to_dict(record)
        anime = record.anime
        anime_dict = model_to_dict(anime) if anime else None
        record_dict['anime'] = anime_dict
        result.append(record_dict)
    # print('=================',result[0])
    return result


def get_user_details(user_id):
    """
    获取用户的详细信息，头像/简介/性别等
    :param user_id:
    :return:
    """
    try:
        # 获取UserInfo记录，并关联User表（确保用户存在）
        user_info = UserInfo.objects.select_related('user').get(user_id=user_id)
    except UserInfo.DoesNotExist:
        return {"error": "用户不存在或未填写详细信息"}

    # 将UserInfo转换为字典
    user_info_dict = model_to_dict(
        user_info,
        fields=['gender', 'photo_url', 'resume', 'animes_like', 'books_like', 'games_like']
    )

    # 补充User模型中的字段（如username）
    user_info_dict['username'] = user_info.user.username  # 从关联的User表获取用户名
    # user_info_dict['email'] = user_info.user.email

    return user_info_dict


def get_user_records(user_id):
    # 获取订阅记录并预加载Anime数据，按时间降序排序
    records = RecordAnime.objects.select_related('anime') \
        .filter(user_id=user_id) \
        .order_by('-time')[:10]

    result = []
    for record in records:
        # 处理可能为空的Anime对象
        anime = record.anime
        anime_name = anime.anime_name

        info_url = anime.info_url

        # 格式化订阅日期
        record_date = record.time.strftime("%Y-%m-%d")

        result.append({
            "anime_name": anime_name,
            "record_date": record_date,
            "info_url": info_url
        })

    return result






