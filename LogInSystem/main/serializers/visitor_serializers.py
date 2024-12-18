from rest_framework import serializers

from django.contrib.auth.models import User


from main.models import Visitor


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class RegisterVisitorSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Visitor
        fields = ('user', 'image')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        print("Here Man")
        visitor = Visitor.objects.create(user=user, **validated_data)
        return visitor


class VisitorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Visitor
        fields = ('id', 'first_name', 'last_name', 'username', 'email')
        extra_kwargs = {
                    'id': {'read_only': True}
            }









