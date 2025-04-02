# Generated by Django 5.M.6 on 2025-03-01 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("myapp", "0002_delete_anime"),
    ]

    operations = [
        migrations.CreateModel(
            name="Anime",
            fields=[
                ("anime_id", models.IntegerField(primary_key=True, serialize=False)),
                ("anime_name", models.CharField(blank=True, max_length=255, null=True)),
                ("info_url", models.CharField(blank=True, max_length=255, null=True)),
                ("score", models.CharField(blank=True, max_length=255, null=True)),
                ("img_url", models.CharField(blank=True, max_length=255, null=True)),
                ("total", models.IntegerField(blank=True, null=True)),
                ("resume", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "anime",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AnimeTag",
            fields=[
                ("relate_id", models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "anime_tag",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="RecordAnime",
            fields=[
                ("record_id", models.AutoField(primary_key=True, serialize=False)),
                ("step", models.IntegerField(blank=True, null=True)),
                ("time", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "record_anime",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("tag_id", models.AutoField(primary_key=True, serialize=False)),
                ("tag_name", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "tag",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=255, null=True)),
                ("gender", models.CharField(blank=True, max_length=10, null=True)),
                ("photo_url", models.CharField(blank=True, max_length=255, null=True)),
                ("resume", models.CharField(blank=True, max_length=255, null=True)),
                ("animes_like", models.IntegerField(blank=True, null=True)),
                ("books_like", models.IntegerField(blank=True, null=True)),
                ("games_like", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "user_info",
                "managed": False,
            },
        ),
    ]
