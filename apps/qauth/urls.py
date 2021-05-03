from django.urls import path, include
from .views import *

urlpatterns = [
    # 第三方注册成功的回调地址
    path('success/', QauthView.as_view(), name='success')
]
