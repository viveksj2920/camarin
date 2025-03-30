import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_signup_success(api_client):
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPassword123"
    }
    response = api_client.post(reverse('signup'), payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_login_success(api_client):
    # Create user manually
    user = User.objects.create_user(username="loginuser", email="login@example.com", password="Password123")

    payload = {
        "username": "loginuser",
        "password": "Password123"
    }
    response = api_client.post(reverse('login'), payload)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_failure_wrong_credentials(api_client):
    payload = {
        "username": "ghostuser",
        "password": "wrongpass"
    }
    response = api_client.post(reverse('login'), payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
