from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from apps.shorter.models import Link
from apps.shorter.v1.serializers.links import LinkSerializer

class CreateShortLinkView(CreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['short_url'] = request.build_absolute_uri(f"/{response.data['short_code']}")
        return response

class ListLinksView(ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

class RedirectToOriginalView(APIView):
    def get(self, request, short_code):
        link = get_object_or_404(Link, short_code=short_code)
        return redirect(link.original_url)
