from django.urls import path, include
app_name = 'authentication'
urlpatterns = [
    path('/v1/', include('apps.authentication.v1.urls'), name='authentication-v1'),

]
