from django.urls import path

from apps.portal.views import portal

urlpatterns = [
    path("", portal.PortalView.as_view()),
]
