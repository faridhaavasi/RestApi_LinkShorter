from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def common_user():
    return User.objects.create_user(
        email='example@gmail.com',
        password='1123',
        is_verify=True
    )


class TestAccounts:
    client = APIClient()

    @pytest.mark.django_db
    def test_get_ProfileView_status_200(self, common_user):
        self.client.force_authenticate(user=common_user)
        response = self.client.get(reverse('accounts:profile-view'))  
        assert response.status_code == 200
