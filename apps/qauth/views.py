from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import View
# django 登录校验
from django.contrib.auth.mixins import LoginRequiredMixin
# social第三方登录校验
from social_django.models import UserSocialAuth


class QauthView(View):
    def get(self, request):
        # 一旦进入视图,数据库接接受第三方的用户数据
        response = redirect(reverse('writer:index'))
        response.set_cookie('is_Login', True)
        return response


'''
vi /home/cat/.virtualenvs/blog/lib/python3.8/site-packages/social_core/actions.py 102
增加cookie信息
'''

'''
/complete/weibo/
?state=rtvOR4eWSArr0UfMzWUyi5XtCdpFciU7&code=cb71cfe84831b0a0bd9ebb783c050e02 
'''
