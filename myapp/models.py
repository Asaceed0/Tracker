# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True)
    anime_name = models.CharField(max_length=255, blank=True, null=True)
    info_url = models.CharField(max_length=255, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    resume = models.CharField(max_length=255, blank=True, null=True)
    release_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anime'


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'



class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    resume = models.CharField(max_length=255, blank=True, null=True)
    animes_like = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'user_info'



class AnimeTag(models.Model):
    relate_id = models.AutoField(primary_key=True)
    anime = models.ForeignKey(Anime, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey(Tag, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anime_tag'



class RecordAnime(models.Model):
    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    anime = models.ForeignKey('Anime', models.DO_NOTHING, blank=True, null=True)
    step = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    score_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'record_anime'



