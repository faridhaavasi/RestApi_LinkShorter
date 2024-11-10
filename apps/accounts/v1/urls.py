from django.urls import path
from apps.account.v1.views.profile import ProfileView, EditProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-view'), 
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),  
]
