from django.urls import re_path, path
from .views import *

urlpatterns = [
    path('', BlogIndexView.as_view(), name='index'),  # 首页
    path('tag/', TagsView.as_view(), name='tags'),  # 标签云
    path('category/', CategoryView.as_view(), name='category'),  # 文章分类
    path('timeline/', TimeLineView.as_view(), name='timeline'),  # 时间线,归档
    path('detail/', DeatilView.as_view(), name='detail'),  # 文章详情信息
]
