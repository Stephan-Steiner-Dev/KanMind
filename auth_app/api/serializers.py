from rest_framework import serializers

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serialize and validate data for user registration."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        """Define the model and fields used for registration."""

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
        """Validate that both entered passwords match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({
                'password': 'Die Passwörter stimmen nicht überein.'
            })

        return data

    def create(self, validated_data):
        """Create and return a new user with a hashed password."""
        validated_data.pop('repeated_password')

        return User.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )


class UserSerializer(serializers.ModelSerializer):
    """Serialize basic user information."""

    class Meta:
        """Define the model and fields exposed by the serializer."""

        model = User
        fields = [
            'id',
            'email',
            'fullname'
        ]