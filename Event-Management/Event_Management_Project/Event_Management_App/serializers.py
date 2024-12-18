from rest_framework import serializers
from .models import User, Manager, Perdorues, Event, PerdoruesJoinsEvent
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
        )


class EventListSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = (
            'manager',
            'title',
            'date',
            'duration',
            'capacity',
            'image',
        )


class PerdoruesSignUpSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Perdorues
        fields = ('user',)

    def create(self, validated_data):
        print(validated_data)
        user_details = dict(validated_data.pop('user'))
        print(user_details)
        user_password = user_details.pop('password')
        user = User.objects.create(is_active=True, password=make_password(user_password), **user_details)
        perdorues = Perdorues.objects.create(user=user)
        return perdorues


class EventCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Event
        fields = (
            'title',
            'date',
            'duration',
            'capacity',
            'image',
        )


class AllEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class PerdoruesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Perdorues
        fields = '__all__'


class PerdoruesJoinsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerdoruesJoinsEvent
        fields = ('event',)


class ManagerChecksRegisteredPerdoruesSerializer(serializers.ModelSerializer):
    perdorues = serializers.StringRelatedField()

    class Meta:
        model = PerdoruesJoinsEvent
        fields = ('perdorues',)


class PerdoruesLogInSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Perdorues
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance)
        user = User.objects.get(username=instance.user)
        user_data = validated_data.pop('user')
        print(instance.user)
        print(instance)
        print(validated_data)
        user_serializer = UserSerializer(instance.user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            instance.save()
            return instance
        return instance
