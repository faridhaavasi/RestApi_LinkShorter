from django.urls import path
from apps.accounts.v1.views.profiile import ProfileView, EditProfileView
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-view'), 
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),  
]
