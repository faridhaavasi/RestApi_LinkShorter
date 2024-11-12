from django.urls import path
from apps.authentication.v1.views.sigin import RegisterView, ConfirmEmailView, RequestPasswordResetView, ResetPasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/confirm/<str:token>', ConfirmEmailView.as_view(), name='confirm-email'),
    path('api/request-restpassword', RequestPasswordResetView.as_view(), name='request-resetpassword'),
    path('api/reset-password/<str:token>', ResetPasswordView.as_view(), name='reset-password'),

    path('api/login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
