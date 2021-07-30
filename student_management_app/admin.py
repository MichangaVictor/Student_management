from student_management_app.models import CustomUser
from django.contrib import admin

# Register your models here.


from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
