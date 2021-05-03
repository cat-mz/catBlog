"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd8(eu&63pwe@no$2-#l@uqxfs3)vs-o0+lki0z02p%17u2g*2='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # app
    'apps.users.apps.UsersConfig',
    'apps.writer.apps.WriterConfig',
    'apps.qauth.apps.QauthConfig',
    # 后台文章编辑
    'mdeditor',
    #     第三方登录
    'social_django',
    # 全局搜索
    'haystack',
    # markdown语法解析
    'markdown_deux'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #     第三方登录配置
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cat_blog',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# 模型类自增
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# 指定本项目用户模型类
AUTH_USER_MODEL = 'users.User'

# 静态资源
STATIC_URL = '/static/'
STATIC_ROOT = '/www/blog/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# 媒体图片，存储位置
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 修改系统的未登录跳转连接
LOGIN_URL = '/user/login'

# redis
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/blog.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'blog': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# 邮箱验证激活用户
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'You email address'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'Your authorization code'
# 收件人看到的发件人
EMAIL_FROM = '云猫客找<You email address>'

# 第三方登录配置项
AUTHENTICATION_BACKENDS = (
    'social.backends.weibo.WeiboOAuth2',
    'social.backends.qq.QQOAuth2',
    'social.backends.weixin.WeixinOAuth2',
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
# 注册成功跳转的页面
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'auth:success'
# 开放平台的应用APPID和SECRET
SOCIAL_AUTH_WEIBO_KEY ='APPID'
SOCIAL_AUTH_WEIBO_SECRET = 'SECRET'
SOCIAL_AUTH_QQ_KEY = 'APPID'
SOCIAL_AUTH_QQ_SECRET = 'SECRET'

SOCIAL_AUTH_GITHUB_KEY = 'APPID'
SOCIAL_AUTH_GITHUB_SECRET = 'SECRET'
SOCIAL_AUTH_GITHUB_USE_OPENID_AS_USERNAME = True
GITHUB_CALLBACK = 'IP/callback'

SOCIAL_AUTH_WEIXIN_KEY = 'APPID'
SOCIAL_AUTH_WEIXIN_SECRET = 'SECRET'

MIDDLEWARE_CLASSES = (
    'pat_to_middleware.SocialAuthExceptionMiddleware',
)

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'
SUIT_CONFIG = {  # suit页面配置
    'ADMIN_NAME': '云猫客栈',  # 登录界面提示
    'LIST_PER_PAGE': 20,  # 表中显示行数
    'MENU': ({'label': u'用户类', 'apps': 'apps',
              'icon': 'icon-user',  # 显示左边菜单的图标
              'models': ('users.User', 'auth.Group')},  # 每一个字典表示左侧菜单的一栏
             {'label': u'文章类', 'apps': 'apps',
              'icon': 'icon-lock',
              'models': ('writer.Article', 'writer.ArticleCategory', 'writer.ArticleSwiper', 'writer.ArticleTags')},
             {'label': u'友联类', 'apps': 'apps',
              'icon': 'icon-edit',  # 显示左边菜单的图标
              'models': ('writer.FriendLink', 'writer.FriendLink')},
             ),
    # label表示name，app表示上边的install的app，models表示用了哪些models
}

# 搜索引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
