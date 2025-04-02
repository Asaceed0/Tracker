"""
信号机制
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserInfo

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当 User 模型保存后，自动创建 UserInfo 记录。
    """
    if created:
        print(f'自动添加用户信息 username:{instance.username}')
        UserInfo.objects.create(
            user=instance,
            username=instance.username,  # 将 User 的 username 同步到 UserInfo
            gender='未知',
            animes_like=0,
            resume='enjoy Asaceed!!',
            photo_url='/static/img/default_avatar/default_avatar1.png'
        )