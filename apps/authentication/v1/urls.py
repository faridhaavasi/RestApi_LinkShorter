from django.urls import path
from apps.authentication.v1.views.sigin import RegisterView, ConfirmEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/confirm', ConfirmEmailView.as_view(), name='confirm'),
    path('api/login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
