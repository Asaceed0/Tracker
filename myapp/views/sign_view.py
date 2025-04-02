from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json



def sign(requset):
    return render(request=requset, template_name='sign.html')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # 后端验证
            if not username or not password:
                return JsonResponse({'status': 'error', 'message': '请填写所有字段'}, status=400)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            return JsonResponse({'status': 'error', 'message': '账号或密码错误'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            print('注册',username,email,password)

            # 后端验证
            errors = []

            if User.objects.filter(username=username).exists():
                errors.append('用户名已存在')
            if User.objects.filter(email=email).exists():
                errors.append('邮箱已被注册')
            if len(password) < 8:
                errors.append('密码至少8位')


            if errors:
                return JsonResponse({'status': 'error', 'message': '<br>'.join(errors)}, status=400)

            # 创建用户
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return JsonResponse({'status': 'success', 'message': '注册成功'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': '注册失败'}, status=500)