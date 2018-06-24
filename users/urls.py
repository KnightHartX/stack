from django.conf.urls import url

from . import user_views

app_name = 'users'
urlpatterns = [
    url(r'^register/', user_views.register, name='register'),
]
