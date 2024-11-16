import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="testpassword",
        is_active=True,
        is_verify=False,
    )


@pytest.mark.django_db
class TestAuthenticationViews:
    def test_register_view(self, client):
        data = {
            "email": "newuser@example.com",
            "password": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = client.post(reverse('authentication:register'), data=data)
        assert response.status_code == 201

    def test_request_password_reset(self, client, user):
        client.force_authenticate(user=user)
        response = client.post(reverse('authentication:request-resetpassword'))
        assert response.status_code == 200

   
    def test_reset_password_valid_token(self, client, user):
        token = str(AccessToken.for_user(user))
        data = {
            "password": "newpassword123",
            "confirm_password": "newpassword123",
        }
        response = client.put(reverse('authentication:reset-password', args=[token]), data=data)
        assert response.status_code == 200

    def test_reset_password_invalid_token(self, client):
        invalid_token = "invalidtoken"
        data = {
            "password": "newpassword123",
            "confirm_password": "newpassword123",
        }
        response = client.put(reverse('authentication:reset-password', args=[invalid_token]), data=data)
        assert response.status_code == 400
        assert "message" in response.data
