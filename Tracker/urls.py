"""
URL configuration for Tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    M. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    M. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    M. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import sign_view, home_view, test_view, \
    more_view, info_view, analysis_view, tags_view, \
    categories_view, other_view, user_info_view

urlpatterns = [

    path("admin/", admin.site.urls),
    path("test/", test_view.my_view),
    path("sign/", sign_view.sign, name='sign'),
    path("home/", home_view.home, name='home'),
    path('more', more_view.more, name='more'),
    path('info/<int:subject_id>/', info_view.subject_info, name='subject_info'),
    path('analysis', analysis_view.analysis, name='analysis'),
    path('tags/', tags_view.tag_collect, name='tag-collect'),
    path('categories/<int:tag_id>/', categories_view.categories, name='categories'),
    path('change_info/', user_info_view.change_info, name='change_info'),
    path('filter/', other_view.filter, name='filter'),


    # api
    path('api/search_tags', other_view.search_tags),
    path('search/', other_view.search_view, name='search'),
    path('logout/', other_view.custom_logout, name='logout'),
    path('api/login/', sign_view.user_login, name='api-login'),
    path('api/register/', sign_view.user_register, name='api-register'),
    path('api/get_tag_stats/', more_view.get_tag_stats, name='api-get-tag-stats'),
    path('delete_record/', more_view.delete_record, name='delete_record'),
    path('resubscribe/', more_view.resubscribe, name='resubscribe'),
    path('update_step/', more_view.update_step, name='update_step'),
    path('update_rating/', more_view.update_rating, name='update_rating'),
    path('api/get_trend_stats/', analysis_view.get_trend_stats),
    path('filter/results/', other_view.filter_results, name='filter-results'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
