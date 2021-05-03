# celery 异步请求解决用户激活
# celery
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from utils.constants import SEND_ACTIVE_IP
import time

# send_email 在任务处理者一端加这几句
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery.task', broker='redis://127.0.0.1:6379/8')

'''todo:启动命令celery -A celery_task.tasks worker -l info'''


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = 'Cat_blog 欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为云猫客栈用户</h1>请点击下面链接激活您的账户<br/><a href="%s/user/active/%s">%s/user/active/%s</a>' % (
        username, SEND_ACTIVE_IP, token, SEND_ACTIVE_IP, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def send_change_password_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = 'Cat_blog 欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 请认真慎重填写密码</h1>请点击下面链接进行修改密码<br/><a href="%s/user/changepassword/%s">%s/user/changepassword/%s</a>' % (
        username, SEND_ACTIVE_IP, token, SEND_ACTIVE_IP, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
