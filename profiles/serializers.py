from rest_framework import serializers

from profiles import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password', 'friends')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""

        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


class MessageSerializer(serializers.ModelSerializer):
    """Serializes messages"""

    class Meta:
        model = models.Messaging
        fields = ('sent_from', 'message_text', 'sent_to', 'sent_on')
        extra_kwargs = {'sent_from': {'read_only': True}}


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializes friends requests"""

    class Meta:
        model = models.FriendRequest
        fields = ('from_user', 'to_user', 'timestamp')
        extra_kwargs = {'from_user': {'read_only': True}}
