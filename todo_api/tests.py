from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser


class AuthTests(TestCase):
    def setUp(self):
        # Initialize API client
        self.client = APIClient()

        # Test user data
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "Test.102892"
        }

        # Create a test user for signin/signout tests
        self.user = CustomUser.objects.create_user(**self.user_data)

    # def test_signup(self):
    #     """Test user signup functionality."""
    #     signup_url = reverse("user-create")  # Djoser signup endpoint
    #     signup_data = {
    #         "email": "newuser@example.com",
    #         "username": "newuser",
    #         "password": "Test.102892"
    #     }

    #     response = self.client.post(signup_url, signup_data, format="json")

    #     # Assert the response is 201 Created
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Check if the user is created in the database
    #     self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_signin(self):
        """Test user signin functionality."""
        signin_url = reverse("login")  # Djoser token login endpoint
        signin_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }

        response = self.client.post(signin_url, signin_data, format="json")

        # Assert the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response contains the authentication token
        self.assertIn("auth_token", response.data)

    def test_signout(self):
        """Test user signout functionality."""
        # Sign in first to get the token
        signin_url = reverse("login")
        signin_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        signin_response = self.client.post(signin_url, signin_data, format="json")
        token = signin_response.data["auth_token"]

        # Authenticate client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Call the logout endpoint
        signout_url = reverse("logout")  # Djoser token logout endpoint
        response = self.client.post(signout_url)

        # Assert the response is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure token is invalidated by making an authenticated request
        protected_url = reverse("task-list-create")  # Example of a protected endpoint
        protected_response = self.client.get(protected_url)
        self.assertEqual(protected_response.status_code, status.HTTP_401_UNAUTHORIZED)
