from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'account'  本来是一定要写这一行，否则html中会报错 'account' is not a registered namespace
# 但在MyBlog的urls.py中，已经将该app_name传入，所以不会遇到该问题

urlpatterns = [
    # path(r'login/', views.user_login, name='user_login'),
    # Django内置的登录方法 LoginView（）函数里有一个默认参数redirect_field_name=LOGIN_REDIRECT_URL，
    # 这就是登录后的重定向设置，我们需要到settings.py设置LOGIN_REDIRECT_URL，登录后重定向到/blog/
    path(r'login/', views.user_login, name='user_login'),
    # 使用Django内置的登出方法
    path(r'loginout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='user_logout'),
    # 图片验证码

    # ^表行开头，\d表数字，+表示至少有一个，$表行结尾，url有匹配正则表达式功能
    url(r'^verify_image/(\d+)/(\d+)/$', views.verify_image, name='verify_image'),
    # 注册
    path(r'register/', views.user_register, name='user_register'),

    # 修改密码
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html",
                                               success_url="/account/password-change-done/"),  # 成功修改则跳转到对应的url
         name='password_change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"),
         name='password_change_done'),

    # 重置密码
    path('password-reset/',  # 重置界面
         auth_views.PasswordResetView.as_view(
             template_name="account/password_reset_form.html",
             email_template_name="account/password_reset_email.html",
             subject_template_name="account/password_reset_subject.txt",
             success_url="/account/password-reset-done/"),
         name='password_reset'),
    path('password-reset-done/',  # 填写完重置信息
         auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',  # 发送重置邮件，uid和token组成url
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",
                                                     success_url='/account/password-reset-complete/'),
         name="password_reset_confirm"),
    path('password-reset-complete/',  # 重置成功
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    # 用户个人信息界面
    path('my-information/', views.myself, name='my_information'),
    # 用户个人信息编辑界面
    path('edit-my-information/', views.myself_edit, name="edit_my_information"),
    # 用户上传图片
    path('my-image/', views.my_image, name="my_image"),


]
