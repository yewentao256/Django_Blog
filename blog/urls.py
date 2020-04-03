from django.urls import path
from . import views

urlpatterns = [
    # 如果不用自定义的方式指定模板位置，Django会在运行时自动去templates查找render()函数中所指定的模板文件。
    path(r'', views.blog_list, name='blog_list'),
    path(r'<int:article_id>/', views.blog_detail, name='blog_detail'),
]