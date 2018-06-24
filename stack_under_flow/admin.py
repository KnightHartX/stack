from django.contrib import admin
from .models import question
from .models import answer
from .models import tag
from users.models import User

# class MyAdminSite(admin.AdminSite):
admin.site.site_header = 'Stack Underflow'
admin.site.site_title = 'Stack Underflow'
# admin_site = MyAdminSite('admin/')

# Register your models here.

@admin.register(question)
class question(admin.ModelAdmin):
    list_display=('update_time','title','contentstring','useridnickname')
    ordering = ['-update_time']

@admin.register(answer)
class answer(admin.ModelAdmin):
    list_display=('update_time','contentstring', 'useridnickname')
    ordering = ['-update_time']

@admin.register(tag)
class tag(admin.ModelAdmin):
    list_display=('id', 'tagname')
    ordering = ['id']


