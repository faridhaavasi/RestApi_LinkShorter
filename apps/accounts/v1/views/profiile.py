from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.v1.serializers.accounts import AccountSerializer, AccountUpdateSerializer
from apps.accounts.models import Account
from apps.accounts.permisions import IsOwnerAccount
class ProfileView(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.account  
    


class EditProfileView(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerAccount]

    def get_object(self):
        return self.request.user.account    