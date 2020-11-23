from django.conf.urls import url

from . import views


app_name = 'custom_requests'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
