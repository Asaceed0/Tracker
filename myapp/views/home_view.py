from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.functions.home_func import get_user_anime_records, get_user_details, get_user_records


def home(request):
    items_anime = get_user_anime_records(request.user.id)
    # print(items_anime)
    user_details = get_user_details(request.user.id)
    # print(user_details)
    recently_record = get_user_records(request.user.id)
    # print(recently_record)

    return render(request, template_name='home.html',
                  context={'items_anime': items_anime[:3], 'user_details': user_details,
                           'recently_record': recently_record})





