from rest_framework import serializers
from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'fullname',
            'email',
            'password',
            'repeated_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({
                'password': 'Die Passwörter stimmen nicht überein.'
            })

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')

        return User.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'fullname'
        ]