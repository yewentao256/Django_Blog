# 登录表单的实现
from django import forms
from django.contrib.auth.models import User
from .models import UserInfo


# 用于登录的表单,有form的话就有自动的检查空白等功能
class LoginForm(forms.Form):
    """
    LoginForm相当于登录表单的html代码
    <tr><th>
    <label for="id_username">Username:</label></th><td><input type="text" name="username" required id="id_username">
    </td></tr>
    <tr><th>
    <label for="id_password">Password:</label></th><td><input type="password" name="password" required id="id_password">
    </td></tr>
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    verify = forms.CharField()


# 用于注册的表单，注意：继承的是ModelForm
# 如果要将表单中的数据写入数据库表或修改某些记录的值，就让表单类继承 forms.ModelForm，否则继承forms.Form
class RegistrationForm(forms.ModelForm):
    # 原模型中没有这两个字段，我们在此处新增
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="ConfirmPassword", widget=forms.PasswordInput)
    phone = forms.CharField(label="Phone")

    class Meta:
        model = User
        fields = ("username", "email")  # 只选用用户名和email字段

    # clean_ +属性名称 命名方式所创建的方法，会在调用表单实例对象的 is_valid()方法时被执行。
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("两次输入的密码不匹配")
        return cd['password2']


# 对自带User模型扩展的表单（详细信息——用户可以修改的片段）
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("phone", "school", "company", "profession", "address", "aboutme", "photo")


# 同上
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # 特别注意：UserForm 的 fields 中不包括 username ，因为 username 一旦确定就不能随便修改，
        # 所以在用户详细信息中不允许修改这个字段。
        fields = ("email",)