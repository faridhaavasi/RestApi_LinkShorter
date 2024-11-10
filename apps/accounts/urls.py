from django.urls import path, include

app_name = 'account'
urlpatterns = [
    path('api/v1/', include('apps.accounts.v1.urls')),
    
]
