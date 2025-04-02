# views.py 新增视图函数
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.models import UserInfo
from django.conf import settings
import os


@login_required
def change_info(request):
    user_info = UserInfo.objects.get(user=request.user)

    if request.method == 'POST':
        # 处理表单数据
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        resume = request.POST.get('resume', '')

        # 验证用户名
        if not username:
            return render(request, 'change_info.html', {
                'user_details': user_info,
                'error': '用户名不能为空'
            })

        # 处理头像
        avatar_file = request.FILES.get('avatar')
        selected_avatar = request.POST.get('selected_avatar')

        if avatar_file:
            # 保存上传的文件
            file_name = f'user_{request.user.id}{os.path.splitext(avatar_file.name)[1]}'
            save_path = os.path.join(settings.MEDIA_ROOT, 'photo', file_name)
            with open(save_path, 'wb+') as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)
            user_info.photo_url = os.path.join(settings.MEDIA_URL, 'photo', file_name)
        elif selected_avatar:
            user_info.photo_url = selected_avatar

        # 更新其他字段
        user_info.username = username
        user_info.gender = gender
        user_info.resume = resume
        user_info.save()

        return redirect('/home')

    return render(request, 'change_info.html', {
        'user_details': user_info
    })