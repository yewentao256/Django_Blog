from django.contrib import admin
from .models import UserInfo


# Register your models here.
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
    list_filter = ("user",)
    search_fields = ("user", "phone")
    raw_id_fields = ("user",)


admin.site.register(UserInfo, UserInfoAdmin)
