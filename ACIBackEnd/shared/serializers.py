from rest_framework import serializers

from shared.models import ACIAdmin, User

class CreateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'first_name', 'last_name', 'email', 'personal_number')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
    

