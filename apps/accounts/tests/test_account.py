from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from apps.accounts.models import Account

User = get_user_model()

@pytest.fixture
def common_user():
    return User.objects.create_user(
        email='example@gmail.com',
        password='1123',
        is_verify=True
    )
@pytest.fixture
def create_account(common_user):
    account, created = Account.objects.get_or_create(user=common_user)
    return account



class TestAccounts:
    client = APIClient()

    @pytest.mark.django_db
    def test_get_ProfileView_status_200(self, common_user):
        self.client.force_authenticate(user=common_user)
        response = self.client.get(reverse('accounts:profile-view'))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_EditProfileView_with_valid_data(self, common_user, create_account):
        data = {
            'bio': 'test',
            'id_user': 'test'
        }
        self.client.force_authenticate(user=common_user)

        response = self.client.put(reverse('accounts:edit-profile'), data=data)
        assert response.status_code == 200  