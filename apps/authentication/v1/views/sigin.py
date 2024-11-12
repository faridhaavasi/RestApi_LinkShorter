from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from apps.authentication.v1.serializers.register import RegisterSerializer
from apps.authentication.utils import EmailSendThread
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
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
