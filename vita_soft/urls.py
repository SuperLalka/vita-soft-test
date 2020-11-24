from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)


tokens_url = [
    path('', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include(tokens_url)),
    path('', include('custom_requests.urls')),
]

