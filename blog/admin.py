from django.contrib import admin
from .models import BlogArticles


class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("publish",)  # 以publish增加一个过滤器，可以根据日期选择显示文章
    search_fields = ("title", "body")  # 可以在title和body中搜索
    raw_id_fields = ("author",)  # 可以显示author的id
    date_hierarchy = "publish"  # 一个可以选择任意日期的过滤器
    ordering = ["publish", "author"]  # 这样设置，publish是除id外的第一键
    # ordering = ["author", "publish"]


admin.site.register(BlogArticles, BlogArticlesAdmin)
