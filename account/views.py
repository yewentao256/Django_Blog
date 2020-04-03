import string
from io import BytesIO
from random import randint
import matplotlib.font_manager as fm # to create font
from PIL import Image, ImageFont, ImageDraw
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserInfoForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import UserInfo
from django.contrib.auth.models import User


# 用于登录的views
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        verify_session = request.session.get('verify', '')
        next_url = request.GET.get('next')
        # login_form.is_valid 在创建实例时，如果传递给表单的数据是符合表单类属性要求的，则返回True，否则返回False
        if not login_form.is_valid():
            message = "对不起，表单无效！"
        # login_form.cleaned_data 以字典的形式返回实例的具体数据。
        # 如果传入的某项数据不合法，则在cleaned_data的结果中不予显示。
        cd = login_form.cleaned_data
        if cd['verify'].lower() == verify_session.lower():
            if User.objects.filter(username=cd['username']):
                user = authenticate(username=cd['username'], password=cd['password'])  # 通过返回user对象
                if user:
                    login(request, user)
                    if next_url and next_url.strip() != '':
                        # 存在next参数的话则跳转到next参数处
                        return HttpResponseRedirect(next_url)
                    else:
                        # 登录成功，跳转到主页
                        return HttpResponseRedirect(reverse("home"))
                else:
                    message = "对不起，您的密码输入有误！"
            else:
                message = "不存在的账户！"
        else:
            message = "验证码错误，请重新输入"
        return render(request, "account/login.html", {"form": login_form, 'message': message})

    # 如果只是浏览，而没有提交任何数据（说明没有点击login）
    else:
        login_form = LoginForm()
        next_url = request.GET.get('next', '')  # 获取url中?next=xx作为参数
        return render(request, "account/login.html", {"form": login_form, 'next_url': next_url})


# 返回验证码图片
def verify_image(request, width, height):
    words_count = 4  # 验证码中的字符长度
    width = int(width)  # 图片宽度
    height = int(height)  # 图片高度
    size = int(min(width / words_count, height) / 1.3)  # 字体大小设置，小于高度且四个字留有余地
    bg_color = (randint(200, 255), randint(200, 255), randint(200, 255))  # 随机背景色（浅色）
    # 第一个参数是颜色通道，这里使用了RGB通道，还有其他的一些通道，如CMYK之类的
    # 第二个参数是由宽高组成的元组，数字
    # 第三个参数是图片的背景色，这里用rgb的颜色显示，例如( 255, 255, 255)，注意这是元组
    img = Image.new('RGB', (width, height), bg_color)  # 创建图像

    # 用到了ImageFont的truetype函数，可以自动查询电脑中的字体
    # 第一个参数是字体名字
    # 第二个参数是字体大小
    # 注意这个是windows系统下默认的字体
    # font = ImageFont.truetype('arial.ttf', size)  # 导入字体
    # 这个使用matplotlib.font_manager生成字体
    font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), size)

    # 用到了ImageDraw的Draw函数
    # 有且只有一个参数，就是之前创建的画布
    draw = ImageDraw.Draw(img)  # # 创建画笔

    # text = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = string.digits + string.ascii_letters  # 数字+大写字母
    verify_text = ''
    for i in range(words_count):
        text_color = (randint(0, 160), randint(0, 160), randint(0, 160))  # 确定文字的颜色，要随机的颜色，颜色要比较深
        # i为第几个文字，例如i=0，size=0.5，width=4时，距离左侧0.25，i=1距离左侧1.25
        left = width * i / words_count + (width / 4 - size) / 2
        top = (height - size) / 2

        word = text[randint(0, len(text) - 1)]
        verify_text += word
        # 写字需要使用draw的text方法
        # 第一个参数是一个坐标轴元组，分别是距离左边和上边的距离
        # 第二个参数是要写的字（字符串）
        # 后面的两个参数分别是字体和字体颜色
        draw.text((left, top), word, font=font, fill=text_color)

    # 随机打上30个*号
    for i in range(30):
        text_color = (255, 255, 255)  # 颜色：白色
        left = randint(0, width)  # 位置：随机
        top = randint(0, height)
        draw.text((left, top), '*', font=font, fill=text_color)

    # 随机画上5条线
    for i in range(5):
        line_color = (randint(0, 160), randint(0, 160), randint(0, 160))  # 颜色：随机
        line = (randint(0, width), randint(0, height), randint(0, width), randint(0, height))  # 位置：头尾都随机
        # 画线条需要使用draw的line方法
        # 第一个参数是包含了两个坐标的元组，分别是线条一头一尾的坐标
        # 后面的参数是线条的颜色
        draw.line(line, fill=line_color)

    # 将画笔删除
    del draw

    # StreamIO，可以将图片缓存到内存里面，读取后就清空内存
    image_stream = BytesIO()  # 建立一个缓存对象
    # print(image_stream)  # 类似于：<_io.BytesIO object at 0x0000022CE22C00F8>
    img.save(image_stream, 'jpeg')  # 将图片保存到内存中
    # print(img, image_stream.getvalue())
    request.session['verify'] = verify_text  # 保存相应的文字在session里面
    return HttpResponse(image_stream.getvalue(), 'image/jpeg')  # 返回内存中的图片


# 用于注册的views
def user_register(request):
    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            # user_form.save(commit=False) 仅生成一个数据对象，不会保存到数据库表
            new_user = register_form.save(commit=False)
            # 这里直接用上User自带的password，就不用model中额外添加
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            UserInfo.objects.create(user=new_user, phone=register_form.cleaned_data['phone'])
            # return HttpResponse("注册成功！")
            # reverse的作用是提取url中“name”的成分，这样无论url如何改动，代码都可以不变，还能加上参数。
            return HttpResponseRedirect(reverse("account:user_login"))  # 直接重定向到login界面
        else:
            return HttpResponse("抱歉，您注册失败了，可能是因为您的密码两次输入不同，或是该用户名已经被使用")
    else:
        register_form = RegistrationForm()
        return render(request, "account/register.html", {"form": register_form})


# 展示用户信息
@login_required(login_url='/account/login')  # 登录需求的修饰器（装饰器）
def myself(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user": user, "userinfo": userinfo})


# 编辑用户信息
@login_required(login_url='/account/login')
def myself_edit(request):
    # 如果有对应属性的话，则获得它，没有则创建它
    if hasattr(request.user, 'userinfo'):
        userinfo = UserInfo.objects.get(user=request.user)
    else:
        UserInfo.objects.create(user=request.user)

    # 一界面双用，如果有post信息，则更新数据
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if userinfo_form.is_valid() * user_form.is_valid():
            user_cd = user_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userinfo.phone = userinfo_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')  # 重定向至用户信息界面
    # 如果只是访问，则返回对应信息
    else:
        user_form = UserForm(instance=request.user)
        userinfo_form = UserInfoForm(
            initial={"phone": userinfo.phone, "school": userinfo.school, "company": userinfo.company,
                     "profession": userinfo.profession,
                     "address": userinfo.address, "aboutme": userinfo.aboutme})
        return render(request, "account/edit_my_infomation.html",
                      {"user_form": user_form, "userinfo_form": userinfo_form, "userinfo": userinfo})


# 上传图像有关操作
@login_required(login_url='/account/login')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("成功上传图片！")
    else:
        return render(request, 'account/imagecrop.html', )
