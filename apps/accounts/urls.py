from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.accounts.v1.urls')),
    
]
