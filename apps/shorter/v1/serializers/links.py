from rest_framework import serializers
from apps.shorter.models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['user', 'original_url', 'short_code']
        read_only_fields = ['user' ,'short_code']
