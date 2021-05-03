from django.contrib import admin
from .models import Article, ArticleCategory, ArticleSwiper, ArticleTags, FriendLink



admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(ArticleSwiper)
admin.site.register(ArticleTags)
admin.site.register(FriendLink)
