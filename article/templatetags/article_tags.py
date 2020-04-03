from django import template
from article.models import ArticlePost
from django.db.models import Count


register = template.Library()  # 注册标签的固定写法


# 返回所有文章计数
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


# 返回作者文章计数，注意，此处传进一个user对象
@register.simple_tag
def author_total_articles(user):
    return user.article.count()


# 显示最新发布的文章
# 一种比较普遍的tag类型是只是渲染其它模块显示下内容，这样的类型叫做Inclusion Tag
@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles": latest_articles}


# 显示评论最多的文章
@register.simple_tag
def most_commented_articles(n=3):
    # annotate：数据聚合函数，这里的作用是将评论最多的文章对象返回
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]
