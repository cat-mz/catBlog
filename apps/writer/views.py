from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Article, ArticleSwiper, ArticleTags, ArticleCategory, FriendLink
from django.core.paginator import Paginator
import logging

logger = logging.getLogger('blog')


class BlogIndexView(View):
    def get(self, request):
        # 轮播图
        swper_list = ArticleSwiper.objects.all()
        # 文章 达到65536数量直接宕机  articles = Article.objects.all()
        #  要多少给多少             id大于查询页数*6    并且小于 查询页数-1小于 *6
        # articles = Article.objects.filter(id__lt=6 * page, id__gt=6 * (page - 1))
        page = request.GET.get('page', 1)
        # hot
        if request.GET.get('hot', ''):
            articles = Article.objects.all().order_by('-total_view')
        else:
            articles = Article.objects.all().order_by('-create_time')
        # 分页器                   5
        paginator = Paginator(articles, 5)
        page = paginator.page(page)
        # 总页数
        page_total = paginator.num_pages

        # 标签云
        tags = ArticleTags.objects.all()
        # 文章分类
        categories = ArticleCategory.objects.all()
        # 友联
        links = FriendLink.objects.all()
        context = {
            'swpers': swper_list,
            'articles': page.object_list,  # 分页返回的查询列表
            'page_total': page_total,
            'page': page,
            'tags': tags,
            'categories': categories,
            'links': links
        }
        return render(request, 'index.html', context=context)


class TagsView(View):
    def get(self, request):
        tagname = request.GET.get('tag')
        page = request.GET.get('page', 1)
        # 以时间最新更新排序
        articles = ArticleTags.objects.get(title=tagname).article.all().order_by('-create_time')
        # 分页器                   5
        paginator = Paginator(articles, 5)
        page = paginator.page(page)
        # 总页数
        page_total = paginator.num_pages
        context = {
            'articles': page.object_list,  # 分页返回的查询列表
            'page_total': page_total,
            'page': page,
        }
        return render(request, 'tags.html', context=context)


class CategoryView(View):
    def get(self, request):
        category = request.GET.get('category')
        print(category)
        page = request.GET.get('page', 1)
        # 以时间最新更新排序
        articles = ArticleCategory.objects.get(title=category).article.all().order_by('-create_time')
        # 分页器                   5
        paginator = Paginator(articles, 5)
        page = paginator.page(page)
        # 总页数
        page_total = paginator.num_pages
        context = {
            'articles': page.object_list,  # 分页返回的查询列表
            'page_total': page_total,
            'page': page,
        }
        return render(request, 'tags.html', context=context)


class TimeLineView(View):
    def get(self, request):
        # 文章过少，不进行处理了分页麻烦死了
        articles = Article.objects.all().order_by('-create_time')
        # 处理年份重复
        year = set()
        for x in articles:
            year.add(x.create_time.year)
        year = list(year)
        year.reverse()
        return render(request, 'timeline.html', {'articles': articles, 'years': year})


class DeatilView(View):
    def get(self, request):
        id = request.GET.get('id')
        try:
            id = int(id)
        except Exception as e:
            logger.error(e)
            return HttpResponse('该文章不存在')
        article = Article.objects.get(id=id)
        # 阅读量访问时 加1
        article.total_view += 1
        article.save()
        return render(request, 'detail.html', {'user': article.content})


'''
过滤器比如类为A
{{ A|date:“m-d” }} 12-02
常见日期格式
[’%Y-%m-%d %H:%M:%S’, # ‘2006-10-25 14:30:59’
‘%Y-%m-%d %H:%M’, # ‘2006-10-25 14:30’
‘%Y-%m-%d’, # ‘2006-10-25’
‘%m/%d/%Y %H:%M:%S’, # ‘10/25/2006 14:30:59’
‘%m/%d/%Y %H:%M’, # ‘10/25/2006 14:30’
‘%m/%d/%Y’, # ‘10/25/2006’
‘%m/%d/%y %H:%M:%S’, # ‘10/25/06 14:30:59’
‘%m/%d/%y %H:%M’, # ‘10/25/06 14:30’
‘%m/%d/%y’] # ‘10/25/06’

'''

