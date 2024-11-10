from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.shorter.v1.urls'), name='shorter-v1'),
]
