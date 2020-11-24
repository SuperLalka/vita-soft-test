from django.conf.urls import url
from django.urls import include

from rest_framework.routers import DefaultRouter
from . import views


routerAPI = DefaultRouter()
routerAPI.register(r'requests', views.RequestsViewSet, basename='requests')
routerAPI.register(r'users', views.UsersViewSet, basename='users')


app_name = 'custom_requests'
urlpatterns = [
    url(r'^api/', include(routerAPI.urls)),
]
