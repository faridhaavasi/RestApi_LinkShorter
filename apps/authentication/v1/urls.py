from django.urls import path
from apps.authentication.v1.views.sigin import RegisterView, ConfirmEmailView

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/confirm', ConfirmEmailView.as_view(), name='confirm'),
]
