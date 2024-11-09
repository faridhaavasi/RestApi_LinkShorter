from tokenize import TokenError
from rest_framework import serializers
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2') 
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False 
        user.save()
        return user


class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            token_obj = RefreshToken(value)
            user_id = token_obj['user_id']
            self.user = User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired token.")
        return value

    def save(self):
        self.user.is_verify = True
        self.user.is_active = True
        self.user.save()
