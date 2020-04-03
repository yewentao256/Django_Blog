from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        # rsplit从字符段末端开始分隔（结果顺序与split不变，分割次数会影响结果），此处只以"."为分界分割一次，然后取扩展名
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("url并没有正确的扩展名")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageForm, self).save(commit=False)   # 调用父类的save方法，未保存到数据库
        image_url = self.cleaned_data['url']
        image_name = '{0}.{1}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())    # title.扩展名
        response = request.urlopen(image_url)   # 打开对应url
        image.image.save(image_name, ContentFile(response.read()), save=False)  # ContentFile创建django的File对象
        if commit:
            image.save()

        return image