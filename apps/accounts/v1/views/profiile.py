from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.account.v1.serializers.accounts import AccountUpdateSerializer, AccountSerializer
from apps.account.models import Account

class ProfileView(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.account  
    


class EditProfileView(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.account    