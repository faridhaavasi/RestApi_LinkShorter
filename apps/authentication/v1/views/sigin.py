from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from apps.authentication.v1.serializers.register import RegisterSerializer, PasswordResettSerializer
from apps.authentication.utils import EmailSendThread
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data['email']

            # Generate confirmation URL
            token = RefreshToken.for_user(user).access_token
            
            
            # Prepare email
            email_obj = EmailMessage(
                subject='Confirm your email',
                body=str(token),
                from_email=settings.EMAIL_HOST_USER,  # Ensure EMAIL_HOST_USER is set in your settings
                to=[user.email]
            )
            
            # Send email in a new thread
            EmailSendThread(email_obj=email_obj).start()
            
            print(token)  # Debug mode
            return Response({'message': 'Registration successful! Please check your email to confirm your account.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    
    def get(self, request, token):
        try:
            token_obj = AccessToken(token)
            user_id = token_obj['user_id']
            user = get_object_or_404(User, id=user_id)
            
            if user.is_verify:
                return Response({'message': 'User email is already verified.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            user.is_verify = True
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:
            return Response({'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)






class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.user.email
        if not email:
            return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({'message': 'User account is not active.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate reset token
            token = AccessToken.for_user(user)
            reset_url = f"/reset-password/:{str(token)}"
            
            # Send email
            email_obj = EmailMessage(
                subject="Password Reset Request",
                body=f"Click the link to reset your password: {reset_url}",
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            EmailSendThread(email_obj=email_obj).start()
            
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'message': 'No user found with this email.'}, status=status.HTTP_404_NOT_FOUND)




class ResetPasswordView(APIView):
    serializer_class = PasswordResettSerializer
    
    def put(self, request, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # Decode token and get user
                token_obj = AccessToken(token)
                user_id = token_obj['user_id']
                user = User.objects.get(id=user_id)
                
                # Update password
                user.set_password(serializer.validated_data['password'])
                user.save()
                
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            
            except Exception:
                return Response({'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
