import sys
from http import HTTPStatus

from django.conf import settings
from django.utils import timezone
from django.views import View

from apps.api.response import SingleResponse
from apps.api.serializers import StatusSerializer


class StatusManagement(View):
    def get(self, request):
        response = StatusSerializer(
            timestamp=timezone.now(),
        )

        if settings.DEBUG:
            response.python = sys.version
            response.version = settings.VERSION
            response.build = settings.BUILD

        return SingleResponse(request, data=response, status=HTTPStatus.OK)
