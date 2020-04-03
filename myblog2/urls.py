from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # 新版django取消了默认namespace，一定要加namespace，这样html文件中才可以访问blog
    # 如果加上namespace，那么include前面的第一个参数需要改为二元组，第二个内容为app_name
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),  # django自带模板
    path('home/', TemplateView.as_view(template_name="home.html"), name='home'),  # django自带模板
    path('article/', include(('article.urls', 'article'), namespace='article')),
    path('image/', include(('image.urls', 'image'), namespace='image')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # 添加允许访问media的url
