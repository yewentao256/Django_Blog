from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'image'

urlpatterns = [
    # 图片列表
    path('list-images/', views.list_images, name="list_images"),
    # 上传图片
    path('upload-image/', views.upload_image, name='upload_image'),
    # 删除图片
    path('del-image/', views.del_image, name='del_image'),
    # 瀑布流式展示图片
    path('images/', views.falls_images, name="falls_images"),
]