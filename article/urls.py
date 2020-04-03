from django.urls import path
from . import views
from django.urls import re_path

# 原则上一定要写这一行，否则html中会报错 'article' is not a registered namespace，
# 当然如果在MyBlog的urls.py中设置了就没有问题
app_name = 'article'
urlpatterns = [
    # 文章栏目
    path('article-column/', views.article_column, name="article_column"),
    # 修改文章栏目
    path('rename-article-column/', views.rename_article_column, name="rename_article_column"),
    # 删除文章栏目
    path('del-article-column/', views.del_article_column, name="del_article_column"),
    # 发表文章
    path('article-post/', views.article_post, name="article_post"),
    # 文章列表
    path('article-list/', views.article_list, name="article_list"),
    # 查看文章（正则表达式匹配）
    re_path('article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),
    # 删除文章
    path('del-article/', views.del_article, name="del_article"),
    # 修改文章
    path('redit-article/<int:article_id>/', views.redit_article, name="redit_article"),
    # 前台展示文章列表
    path('list-article-titles/', views.article_titles, name="article_titles"),
    # 前台展示具体文章信息
    path('article-content/<int:id>/<slug:slug>/', views.article_detail, name="article_content"),
    # 显示某一作者的全部文章信息
    path('list-article-titles/<username>/', views.article_titles, name="author_articles"),
    # 点赞文章
    path('like-article/', views.like_article, name="like_article"),
    # 文章标签
    path('article-tag/', views.article_tag, name="article_tag"),
    # 删除文章标签
    path('del-article-tag/', views.del_article_tag, name="del_article_tag"),
]
