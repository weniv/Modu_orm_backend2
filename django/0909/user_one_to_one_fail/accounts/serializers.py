from rest_framework import serializers
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source="profile.bio", required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "bio")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance = super().update(instance, validated_data)

        if profile_data:
            instance.profile.bio = profile_data.get("bio", instance.profile.bio)
            instance.profile.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "bio")

    def create(self, validated_data):
        bio = validated_data.pop("bio", "")
        user = User.objects.create_user(**validated_data)
        user.profile.bio = bio
        user.profile.save()
        return user
