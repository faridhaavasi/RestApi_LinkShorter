from rest_framework import serializers
from apps.accounts.models import Account
from apps.shorter.models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['user', 'orginal_url', 'short_code']

class AccountSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['user', 'bio', 'id_user', 'links']

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['bio']
