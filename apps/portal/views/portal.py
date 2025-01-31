from django.shortcuts import render
from django.template.defaultfilters import register
from django.views import View

from apps.core.models import SiteSetting, Project


@register.filter(name="split")
def split(value, key):
    """
    Returns the value turned into a list.
    """
    return value.split(key)


class PortalView(View):
    def get(self, request):
        context = {
            "site_setting": SiteSetting.objects.filter(is_active=True).first(),
            "projects": Project.objects.filter(is_hidden=False).order_by("position", "created_at"),
        }

        return render(request, "portal/index.html", context)
