import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from article.forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm, CommentForm
from .models import ArticleColumn, ArticlePost, ArticleTag


@login_required(login_url='/account/login/')
@csrf_exempt  # 一种django的加密机制，减少csrf攻击
def article_column(request):
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user=request.user, column=column_name)  # 遍历检索是否有重复的栏目名
        if columns:
            return HttpResponse("该栏目名已存在！")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("成功创建！")
    else:
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, 'column_form': column_form})


@login_required(login_url='/account/login')
@require_POST  # 修饰器，只能是POST访问
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("成功修改")
    except:
        return HttpResponse("失败")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("删除成功")
    except:
        return HttpResponse("删除失败")


# 发布文章
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)  # 此时还未上传到数据库
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']  # tags以json包形式传递
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("成功上传")
            except:
                return HttpResponse("表单有效，但上传失败")
        else:
            return HttpResponse("表单无效")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, "article/column/article_post.html",
                      {"article_post_form": article_post_form,
                       "article_columns": article_columns, "article_tags": article_tags})  # 此处传参html中可以用到


# 展示文章列表
@login_required(login_url='/account/login')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 10)  # django自带分页器，参数表示每页显示几条
    page = request.GET.get('page')
    try:  # 尝试获取当前页
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:  # 如果页面非整数，返回第一页
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:  # 如果遇见空页，则返回最后一页
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page})


# 展示具体文章
@login_required(login_url='/account/login')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


# 删除具体文章
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("删除成功")
    except:
        return HttpResponse("删除失败")


# 修改文章
@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_column = article.column
        return render(request, "article/column/redit_article.html",
                      {"article": article, "article_columns": article_columns,
                       "this_article_column": this_article_column, "this_article_form": this_article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("修改成功")
        except:
            return HttpResponse("修改失败")


# 文章标签页面
@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html",
                      {"article_tags": article_tags, "article_tag_form": article_tag_form})

    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("成功上传")
            except:
                return HttpResponse("保存发生异常")
        else:
            return HttpResponse("表单无效")


# 删除文章标签
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("成功删除")
    except:
        return HttpResponse("删除失败")


# 前台展示文章列表, 如果传进username则表示只展示某一作者的全部文章
def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:  # 尝试获取用户详细资料
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()  # 所有上传的博客
    paginator = Paginator(articles_title, 10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, "article/list/author_articles.html",
                      {"articles": articles, "page": current_page, "userinfo": userinfo, "user": user})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})


# 前台文章具体信息
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # total_views = r.incr("article:{}:views".format(article.id))
    # import redis
    # from django.conf import settings
    # 注：用redis统计文章访问量较快，大型网站常用。此处个人博客不用，省的每次开redis服务器
    # r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    # r.zincrby('article_ranking', 1, article.id)  # 每次访问时，自增article_ranking里对应article_id的分数

    # 按照索引范围获取name对应的有序集合的元素，0~-1表示从开头到结尾，排序规则desc=True表示从大到小
    # article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
    # article_ranking_ids = [int(id) for id in article_ranking]  # 对字典而言，直接for的话取的是key

    # most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))  # id__in可以传进列表一次取值
    # most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))  # 用id排序

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()  # get方法的话，直接创建表单返回
        article.views += 1
        article.save(update_fields=['views'])  # 存进数据库

    most_viewed_articles = ArticlePost.objects.all().order_by('-views')[:4]  # 以views数量降序排序

    article_tags_ids = article.article_tag.values_list("id", flat=True)  # 得到当前对象(article_tag是一个对象）的指定字段值
    # exclude排除id相同的文章
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    # 聚合，取4篇相似文章，依照最新和相同标签两种排序方式
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]

    # return render(request, "article/list/article_content.html",
    # {"article": article, "total_views": total_views,
    # "most_viewed": most_viewed, "comment_form": comment_form, "similar_articles": similar_articles})
    return render(request, "article/list/article_content.html",
                  {"article": article, "total_views": article.views,
                   "most_viewed_articles": most_viewed_articles, "comment_form": comment_form,
                   "similar_articles": similar_articles})


# 点赞功能
@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)  # 自带检索重复功能
                return HttpResponse("点赞成功")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("点赞取消")
        except:
            return HttpResponse("不存在的文章id")
    else:
        return HttpResponse("错误的传入参数")
