from django.urls import path

from .views.tweets import TweetView
from .views.users import RegisterView, ConfirmEmailView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'tweets'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('confirm_email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tweets/', TweetView.as_view(), name='tweets'),
]
