from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Role


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    class Meta:
        model  = User
        fields = ('email', 'full_name', 'password', 'password2', 'role')
        extra_kwargs = {
            'role': {'required': False}  # defaults to viewer if not provided
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Read serializer — used to return user data in responses."""

    class Meta:
        model  = User
        fields = ('id', 'email', 'full_name', 'role', 'is_active', 'created_at')
        read_only_fields = fields


class UpdateUserSerializer(serializers.ModelSerializer):
    """Used by admin to update role or active status."""

    class Meta:
        model  = User
        fields = ('role', 'is_active')

    def validate_role(self, value):
        if value not in Role.values:
            raise serializers.ValidationError(f'Role must be one of: {Role.values}')
        return value