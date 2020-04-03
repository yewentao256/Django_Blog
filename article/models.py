from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
from django.urls import reverse


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name='article_column', on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


# 文章标签
class ArticleTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag")
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    # related_name = article，那么就可以通过user.article访问ArticlePost这个类
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)  # 用于生成友好的url，如空格换成-而不是%20
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    # 点赞功能，一篇文章可能多个用户喜欢，一个用户也可以喜欢多篇文章，所以是多对多
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    # 和文章标签对应起来（多对多）
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)
    views = models.IntegerField(blank=True, default=0)  # 浏览数

    class Meta:
        ordering = ("-updated",)  # 按照文章发布时间倒序排列
        # index_together = (('id', 'slug'),) 对数据库中的这两个字段建立索引，
        # 以后就可以通过每篇文章的id和slug来获取该文章对象了，这样建立索引以后，能提高读取文章对象的速度。
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    # save() 每个数据模型类都有一个save方法，在本类中对这个方法重写，
    # 是为了实现 self.slug = slugify(self.title)，然后再执行父类的save方法
    def save(self, *args, **kargs):
        self.slug = slugify(self.title)  # 友好化title字符串
        super(ArticlePost, self).save(*args, **kargs)

    # 获取某篇文章的url，使用reverse针对名称进行url绑定（需要登录）
    # 因为它使用了views.py中的article_detail方法，我们于此加了一个修饰器，login_required
    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])

    # 获取某篇文章的url，使用reverse针对名称进行url绑定（不需要登录）
    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])


# 评论
class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")  # 一篇文章多篇评论
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator, self.article)
