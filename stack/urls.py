"""stack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from users import user_views
from stack import settings
from django.views.static import serve
from stack_under_flow import stack_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 别忘记在顶部引入 include 函数
    url(r'^$', stack_views.displayquestion, name='index'),
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^stack_under_flow/',include('stack_under_flow.urls')),
    path('likes/', include('likes.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),  # 用于上传图片文件
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),  # 用于加载静态文件
]



