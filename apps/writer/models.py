from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone
from apps.users.models import User
from db.base_mode import BaseModel


class Article(BaseModel, models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章图片
    picture = models.ImageField(upload_to='picture/%Y%m%d%h', blank=True)
    # 文章标题
    title = models.CharField(max_length=150)
    # markdown 文章正文
    content = MDTextField()
    # 文章摘要
    sumary = models.CharField(max_length=150, blank=False, null=False)
    # 是否置顶
    top = models.BooleanField(default=False)
    total_view = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_article'
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name


class ArticleCategory(models.Model):
    '''文章分栏'''
    title = models.CharField(max_length=150, verbose_name='文章分栏')
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    # 多对多
    article = models.ManyToManyField(Article)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'
        verbose_name = '文章分栏管理'
        verbose_name_plural = verbose_name


class ArticleTags(models.Model):
    '''标签云'''
    title = models.CharField(max_length=150, verbose_name='标签云')
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    # 多对多
    article = models.ManyToManyField(Article)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_tags'
        verbose_name = '标签云管理'
        verbose_name_plural = verbose_name


class ArticleSwiper(models.Model):
    title = models.CharField(max_length=100)
    # 轮播图
    picture = models.ImageField(upload_to='swiper/%Y%m%d%h', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_swiper'
        verbose_name = '轮播图管理'
        verbose_name_plural = verbose_name


class FriendLink(models.Model):
    title = models.CharField(max_length=150, null=False, unique=True)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_links'
        verbose_name = '友联管理'
        verbose_name_plural = verbose_name
