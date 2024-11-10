from django.urls import path
from apps.shorter.v1.views.links_views import CreateShortLinkView, ListLinksView, RedirectToOriginalView

urlpatterns = [
    path('api/create/', CreateShortLinkView.as_view(), name='create_short_link'),
    path('api/my-links/', ListLinksView.as_view(), name='list_links'),
    path('<str:short_code>/', RedirectToOriginalView.as_view(), name='redirect_to_original'),
]
