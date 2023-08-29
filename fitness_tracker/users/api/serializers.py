from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers

from fitness_tracker.users.models import FitnessProfile

User = get_user_model()


class FitnessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessProfile
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    fitness_profile = FitnessProfileSerializer()

    class Meta:
        model = User
        fields = ("name", "fitness_profile")

    def create(self, validated_data):
        fitness_profile = validated_data.pop("fitness_profile")

        random_username = self.generate_random_username()
        user = self.Meta.model.objects.create(username=random_username, **validated_data)

        FitnessProfile.objects.create(user=user, **fitness_profile)
        return user

    def generate_random_username(self):
        while True:
            random_username = get_random_string(length=16)
            if not self.Meta.model.objects.filter(username=random_username).exists():
                break

        return random_username
