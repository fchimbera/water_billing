from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['account_id', 'email', 'username', 'password', 'password_confirm', 'first_name', 'last_name', 'role']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    account_id_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        account_id_or_email = data.get('account_id_or_email')
        password = data.get('password')
        user = authenticate(username=account_id_or_email, password=password)
        if not user:
            user = authenticate(email=account_id_or_email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account_id', 'email', 'username', 'first_name', 'last_name', 'role']
        read_only_fields = ['account_id', 'email', 'role']