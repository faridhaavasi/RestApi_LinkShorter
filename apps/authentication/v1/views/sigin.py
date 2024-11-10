from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.v1.serializers.register import RegisterSerializer, ConfirmEmailSerializer
from apps.authentication.utils import EmailSendThread
from django.conf import settings


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data['email']

            # Generate confirmation URL
            token = RefreshToken.for_user(user).access_token
            confirmation_url = f"http://localhost:8000/confirm-email/{token}/"
            
            # Prepare email
            email_obj = EmailMessage(
                subject='Confirm your email',
                body=f'Please click the link to confirm your email: {confirmation_url}',
                from_email=settings.EMAIL_HOST_USER,  # Ensure EMAIL_HOST_USER is set in your settings
                to=[user.email]
            )
            
            # Send email in a new thread
            EmailSendThread(email_obj=email_obj).start()
            
            print(token)  # Debug mode
            return Response({'message': 'Registration successful! Please check your email to confirm your account.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(GenericAPIView):
    serializer_class = ConfirmEmailSerializer
    
    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Email confirmed successfully!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
