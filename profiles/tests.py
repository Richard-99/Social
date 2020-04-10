from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

from .models import UserProfile, ProfileFeedItem
from .views import UserProfileFeedViewSet, MessagingViewSet

class UserProfileTest(APITestCase):

    def test_create_profile(self):
        """Ensuring creating a profile"""
        data = {
            "email": "abc@xyz.com",
            "name": "Test user",
            "password": "abc123"
        }
        response = self.client.post(reverse('api:profile-list'), data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().name, 'Test user')


class ProfileFeedItemTest(APITestCase):

    def setUp(self):

        user = UserProfile.objects.create_user(email="abc@xyz.com",
                                                name="Test user",
                                                password="abc123")
        self.url = reverse('api:feed-list')
        self.factory = APIRequestFactory()
        self.view = UserProfileFeedViewSet.as_view({'get': 'list'})
        self.user = UserProfile.objects.get(name="Test user")
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_status_update(self):

        request = self.factory.get(self.url, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MessageItemTest(APITestCase):

    def setUp(self):

        user = UserProfile.objects.create_user(email="abc@xyz.com",
                                                name="Test user",
                                                password="abc123")
        self.url = reverse('api:message-list')
        self.factory = APIRequestFactory()
        self.view = MessagingViewSet.as_view({'get': 'list'})
        self.user = UserProfile.objects.get(name="Test user")
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_status_update(self):

        request = self.factory.get(self.url, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
