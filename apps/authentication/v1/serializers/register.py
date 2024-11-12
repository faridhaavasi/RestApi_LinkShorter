from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import TokenError

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


# class ConfirmEmailSerializer(serializers.Serializer):
#     token = serializers.CharField()

    # def validate_token(self, value):
    #     try:
    #         token_obj = AccessToken(value)
    #         user_id = token_obj['user_id']
    #         self.user = User.objects.get(id=user_id)
    #         if self.user.is_verify:
    #             raise serializers.ValidationError("User email is already verified.")
    #         if not self.user.is_active:
    #             raise serializers.ValidationError("User account is not active.")
    #     except TokenError as e:
    #         raise serializers.ValidationError(f"Token error: {str(e)}")
    #     except Exception:
    #         raise serializers.ValidationError("Token is invalid or expired.")
    #     return value


  

    # def save(self):
    #     self.user.is_verify = True
    #     self.user.is_active = True
    #     self.user.save()



class PasswordResettSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
