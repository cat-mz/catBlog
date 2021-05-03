# Generated by Django 2.1.15 on 2021-05-01 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('picture', models.ImageField(blank=True, upload_to='picture/%Y%m%d%h')),
                ('title', models.CharField(max_length=150)),
                ('content', mdeditor.fields.MDTextField()),
                ('sumary', models.CharField(max_length=150)),
                ('total_view', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文章管理',
                'verbose_name_plural': '文章管理',
                'db_table': 'tb_article',
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='文章分栏')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('article', models.ManyToManyField(to='writer.Article')),
            ],
            options={
                'verbose_name': '文章分栏管理',
                'verbose_name_plural': '文章分栏管理',
                'db_table': 'tb_category',
            },
        ),
        migrations.CreateModel(
            name='ArticleSwiper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('picture', models.ImageField(blank=True, upload_to='swiper/%Y%m%d%h')),
            ],
            options={
                'verbose_name': '轮播图管理',
                'verbose_name_plural': '轮播图管理',
                'db_table': 'tb_swiper',
            },
        ),
        migrations.CreateModel(
            name='ArticleTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='标签云')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('article', models.ManyToManyField(to='writer.Article')),
            ],
            options={
                'verbose_name': '标签云管理',
                'verbose_name_plural': '标签云管理',
                'db_table': 'tb_tags',
            },
        ),
    ]
