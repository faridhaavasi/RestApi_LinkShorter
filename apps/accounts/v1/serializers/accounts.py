from rest_framework import serializers
from apps.account.models import Account
from apps.shorter.models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['original_url', 'short_url']
        read_only_fields = fields

class AccountSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['user', 'bio', 'id_user', 'links']

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['bio']
