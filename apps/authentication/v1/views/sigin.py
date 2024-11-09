from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.v1.serializers.register import RegisterSerializer, ConfirmEmailSerializer
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user).access_token
            confirmation_url = f"http://localhost:8000/confirm-email/{token}/"
            send_mail(
                'Confirm your email',
                f'Please click the link to confirm your email: {confirmation_url}',
                'no-reply@example.com',
                [user.email]
            )
            print(token) # mode debug
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
