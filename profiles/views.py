from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles import models, serializers, permissions

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication token"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating and updating status updates"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged user"""

        serializer.save(user_profile=self.request.user)


class MessagingViewSet(viewsets.ModelViewSet):
    """Handle creating messages"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.MessageSerializer
    queryset = models.Messaging.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets user to the logged in user"""

        serializer.save(sent_from=self.request.user)


class FriendRequestViewSet(viewsets.ModelViewSet):
    """Handling friend requests"""

    User = settings.AUTH_USER_MODEL

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.FriendRequestSerializer
    queryset = models.FriendRequest.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets user to the logged in user"""

        serializer.save(from_user=self.request.user)

    def send_friend_request(self, request, id):
        """View for sending friend request to users"""

        if request.user.is_authenticated():
            user = get_object_or_404(User, id=id)
            frequest, created = FriendRequest.objects.get_or_create(
                from_user=request.user,
                to_user=user
            )

    def cancel_friend_request(self, request, id):
        """View for canceling friend requests"""

        if request.user.is_authenticated():
            user = get_object_or_404(User, id=id)
            frequest = FriendRequest.objects.filter(
                from_user=request.user,
                to_user=user
            ).first()
            frequest.delete()

    def accept_friend_request(self, request, id):
        """View for accepting friend requests"""

        from_user = get_object_or_404(User, id=id)
        frequest = FriendRequest.objects.filter(
            from_user=from_user,
            to_user=request.user
        ).first()
        user1 = frequest.to_user
        user2 = from_user
        user1.profile.friends.add(user2.profile)
        user2.profile.friends.add(user1.profile)
        frequest.delete()

    def delete_friend_request(self, request, id):
        """View for deleting friend requests"""

        from_user = get_object_or_404(User, id=id)
        frequest = FriendRequest.objects.filter(
            from_user=from_user,
            to_user=request.user
        ).first()
        frequest.delete()
