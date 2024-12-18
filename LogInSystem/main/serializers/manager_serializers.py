from rest_framework import serializers

from django.contrib.auth.models import User

from main.models import Manager
from main.serializers.visitor_serializers import UserRegisterSerializer


class ManagerRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Manager
        fields = ('user', 'image')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        obj = Manager.objects.create(user=user, **validated_data)
        return obj
