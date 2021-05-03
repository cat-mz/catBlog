from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.response_code import RETCODE
from utils.constants import SEND_EMAIL_ACTIVE_TIMEOUT, SENED_EMAIL_CHANGE_PASSWOED_TIMEOUT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from .models import User
from celery_task.tasks import send_register_active_email, send_change_password_email
import json
import re
import logging

logger = logging.getLogger('blog')


class UserLoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            is_Login = request.COOKIES.get('is_Login')
            checked = 'checked'
        else:
            username = is_Login = checked = ''
        return render(request, 'login.html', {'username': username, 'is_Login': is_Login, 'checked': checked})

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        if not all([username, password]):
            return HttpResponse('缺少必须的参数')

        user = authenticate(username=username, password=password)

        if user != None:
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)
                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                next_url = request.GET.get('next', redirect('/'))
                # 跳转到next_url
                response = redirect('/')
                if remember == 'on':
                    # 记住用户：None表示两周后过期
                    request.session.set_expiry(None)
                    response.set_cookie('is_Login', True, max_age=14 * 24 * 3600)
                else:
                    request.session.set_expiry(0)
                    response.set_cookie('is_Login', True)
                response.set_cookie('username', username, max_age=14 * 24 * 3600)
                return response
            else:
                return HttpResponse('该用户尚未激活，请前往邮箱进行激活！')
        else:
            return HttpResponse('用户名或密码错误！')


class UserLogoutView(View):
    def get(self, request):
        # 清除用户的session信息
        logout(request)
        response = redirect('/')
        # 退出登录时清除cookie中的登录状态
        response.delete_cookie('is_Login')
        try:  # 清楚第三方登录的cookie信息
            response.delete_cookie('name')
        except Exception as e:
            logger.error(e)
            return
        return response


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取json数据
        data_json = request.body
        # 转化字典格式
        data_set = json.loads(data_json)
        username = data_set['username']
        pwd = data_set['password']
        pwd2 = data_set['password2']
        email = data_set['email']
        code = data_set['code']
        uuid = data_set['uuid']
        if not all([username, pwd, pwd2, email, code, uuid]):
            return JsonResponse({'errno': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必须的参数'})
        if pwd != pwd2:
            return JsonResponse({'errno': RETCODE.PWDERR, 'errmsg': '两次密码不一致，请重新输入'})

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return JsonResponse({'errno': RETCODE.EMAILERR, 'errmsg': '邮箱格式错误'})

        redis_con = get_redis_connection()
        try:
            img_code = redis_con.get('img:%s' % uuid).decode()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'errno': RETCODE.DATABASESERR, 'errmsg': '服务器繁忙，请稍候'})
        if img_code is None:
            return JsonResponse({'errno': RETCODE.IMAGECODEERR, 'errmsg': '验证码已失效'})

        if img_code.lower() != code.lower():
            return JsonResponse({'errno': RETCODE.IMAGECODEERR, 'errmsg': '验证码错误，请重新输入'})
        try:
            if User.objects.filter(username=username):
                return JsonResponse({'errno': RETCODE.USERERR, 'errmsg': '该用户已经存在'})
            user = User.objects.create_user(username=username, password=pwd2, email=email)
            user.is_active = 0
            user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'errno': RETCODE.DATABASESERR, 'errmsg': '服务器繁忙，请稍候'})

        # 组织激活邮箱信息
        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密
        # 加密用户的身份信息，生成激活token               秒
        serializer = Serializer(settings.SECRET_KEY, SEND_EMAIL_ACTIVE_TIMEOUT)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        # 发邮件
        send_register_active_email.delay(email, username, token)

        return JsonResponse({'errno': RETCODE.OK, 'errmsg': '请于三分钟之内到邮箱激活用户'})


class UserActiveView(View):

    def get(self, request, token):
        # 进行解密，获取要激活的用户信息           3分钟
        serializer = Serializer(settings.SECRET_KEY, SEND_EMAIL_ACTIVE_TIMEOUT)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('users:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期,请重新注册')


class ForgetpasswordView(View):

    def get(self, request):
        return render(request, 'changepassword.html')

    def post(self, request):
        data_JSON = json.loads(request.body)
        email = data_JSON['email']
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'errno': RETCODE.EMAILERR, 'errmsg': '邮箱格式错误'})
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'errno': RETCODE.EMAILERR, 'errmsg': '该邮箱不存在，请注册使用'})
            # 进行编码加密防止，降低风险         3600 s == 60m = 1 day
        serializer = Serializer(settings.SECRET_KEY, SENED_EMAIL_CHANGE_PASSWOED_TIMEOUT)
        info = {'user': user.id}
        token = serializer.dumps(info).decode()  # 加密，并解码
        send_change_password_email(email, user.username, token)

        return JsonResponse({'errno': RETCODE.OK, 'errmsg': '请于三分钟之内到邮箱修改密码'})


# 存储修改密码的user id
users_id = []


class ChangePasswordView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, SENED_EMAIL_CHANGE_PASSWOED_TIMEOUT)
        try:
            info = serializer.loads(token)
            user_id = info['user']
            users_id.append(user_id)
        except Exception as e:
            logger.error(e)
            return HttpResponse('激活链接已过期,请再次进行修改密码')
        context = {
            'changepassword': 'users:changepassword'
        }
        return render(request, 'changepassword.html', context=context)


class PasswordSetView(View):
    def post(self, request):
        password = request.POST.get('password')
        # 获取用户id，并进行清除
        for user_id in users_id:
            users_id.pop()
        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()
        return HttpResponse('密码修改成功')


class UserAboutView(View):
    def get(self, request):
        users_desc = User.objects.get(username='admin')
        return render(request, 'about.html', {'user': users_desc.user_desc})


class UserCenterView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user = User.objects.get(username=user)
        context = {
            'user': user
        }
        return render(request, 'center.html', context=context)

    def post(self, request):
        user = request.user
        user = User.objects.get(username=user)
        avatar = request.FILES.get('avatar')
        user_desc = request.POST.get('desc')
        if avatar:
            user.avatar = avatar

        if user_desc:
            print('12345656')
            user.user_desc = user_desc

        user.save()
        return redirect(reverse('users:center'))


# 404
def page_not_found(request, exception):  # 注意点 ①
    return render(request, '404.html')
