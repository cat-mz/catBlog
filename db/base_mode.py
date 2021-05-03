from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """模型抽象基类使所有模型类继承这些字段"""
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明是一个抽象模型类
        abstract = True
