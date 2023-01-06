from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token

from .views import *

urlpatterns = [
    path('auth', AuthAPIView.as_view()),
    path('api-token-verify', verify_jwt_token),
    path('api-token-refresh', refresh_jwt_token),

    path('change-password', ChangePasswordView.as_view()),

    path('student', StudentCreateAPIView.as_view()),
    path('student/<int:id>', StudentCreateAPIView.as_view()),

    path('category', CategoryListAPIView.as_view()),
    path('category/<int:id>', CategoryDetailAPIView.as_view()),

    path('courses', CourserListApiView.as_view()),
]
