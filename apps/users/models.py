from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_mode import BaseModel
from mdeditor.fields import MDTextField


class User(AbstractUser, BaseModel):
    # 用户头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d%h', blank=True)
    user_desc = MDTextField()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


'''
User对象的字段:
password：Django默认保存是加密后的密码，无法直接看到明文密码
last_login：上一次登陆时间
is_superuser：是否是超级管理员，是为1，否为0
username：用户名
first_name
last_name
email：邮箱
is_staff：用户是否拥有网站的管理权限
is_active：是否允许用户登录, 设置为 False，可以在不删除用户的前提下禁止用户登录。
data_joined：账户创建日期
groups： 与组多对多关联的字段
user_permissions： 与权限关联的多对多字段，也就是是说明了为什么第三张表表为auth_user_user_permissions. 
表名（user）+字段名（user_permissions）
'''

'''
类属性:
is_authenticated：判断是否被认证，即是否登陆
is_anonymous： 是否为匿名用户
username_validator：指向用于验证用户名的验证实例，默认是validators.UnicodeUsernameValidator
'''

'''
类方法:
get_username()：  获取用户名
get_full_name()： 获取全名，即first_name+空格+last_name
get_short_name()：获取first_name
set_password(raw_password)： 设置密码,如果raw_password是None，则密码将被设置为不可用的密码，就像使用了 set_unusable_password() 一样。
check_password(raw_password)： 检查密码是否正确。
set_unusable_password()：将用户标记为未设置密码，即密码为None
has_usable_password()：返回该用户是否未设置密码
get_group_permissions()： 获取这个用户所在组中所具有的的全部权限。
has_perm()： 判断一个用户是否具有某个权限。
has_perms(perm_list)： 判断用户对一个权限列表是否具有权限。
has_module_perms(package_name)： 判断对app是否有权限。
'''
