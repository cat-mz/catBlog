from django.urls import path, re_path
from .views import *
from .verify_code import Capcha

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # 登录
    path('register/', UserRegisterView.as_view(), name='register'),  # 注册
    path('imagecode', Capcha.as_view(), name='imagecode'),  # 图片验证码
    re_path(r'^changepassword/(?P<token>.*)$', ChangePasswordView.as_view(), name='changepassword'),  # 发送邮箱修改
    path('password/', PasswordSetView.as_view(), name='passwordset'),  # 设置密码
    path('forgetpassword/', ForgetpasswordView.as_view(), name='forgetpassword'),  # 找回密码
    re_path(r'^active/(?P<token>.*)$', UserActiveView.as_view(), name='active'),  # 用户激活
    path('logout/', UserLogoutView.as_view(), name='logout'),  # 退出登录
    path('about/', UserAboutView.as_view(), name='about'),  # 关于
    path('center/', UserCenterView.as_view(), name='center'),  # 个人中心
]
