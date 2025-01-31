from django.contrib import admin
from django.db import models
from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext as _
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from apps.core.models import Project, ProjectImage, SiteSetting, ProjectImageRow


class HttpResponseRedirectToReferrer(HttpResponseRedirect):
    def __init__(self, request, *args, **kwargs):
        redirect_to = request.META.get("HTTP_REFERER", "/")
        super().__init__(redirect_to, *args, **kwargs)


class ProjectImageAdmin(NestedStackedInline):
    model = ProjectImage
    formfield_overrides = {  # added
        models.PositiveIntegerField: {"widget": HiddenInput()},  # added
    }
    sortable_field_name = "position"
    fields = ["content", "position"]
    readonly_fields = ["mime", "created_at"]
    extra = 0


class ProjectImageRowAdmin(NestedStackedInline):
    model = ProjectImageRow
    formfield_overrides = {  # added
        models.PositiveIntegerField: {"widget": HiddenInput()},  # added
    }
    sortable_field_name = "position"
    inlines = [ProjectImageAdmin]
    fields = ["position"]
    extra = 0


class ProjectAdmin(NestedModelAdmin):
    list_display = ("id", "position", "title", "subtitle", "is_hidden", "created_at", "updated_at", "sort_actions")
    search_fields = ("title", "subtitle", "url_name")
    fields = [
        "title",
        "subtitle",
        "year",
        "text_top",
        "text_bottom_left",
        "text_bottom_right",
        "cover",
        "is_hidden",
        "position",
    ]
    show_facets = admin.ShowFacets.ALWAYS

    inlines = [ProjectImageRowAdmin]

    def save_model(self, request, obj, form, change):
        if not obj.url_name:
            obj.url_name = slugify(obj.title)
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "projects/<int:project_id>/sort-up",
                self.admin_site.admin_view(self.process_up),
                name="project-up",
            ),
            path(
                "projects/<int:project_id>/sort-down",
                self.admin_site.admin_view(self.process_down),
                name="project-down",
            ),
        ]
        return custom_urls + urls

    def process_up(self, request, project_id, *args, **kwargs):
        project = self.get_object(request, project_id)
        project.position += 1
        project.save()
        return HttpResponseRedirectToReferrer(request)

    def process_down(self, request, project_id, *args, **kwargs):
        project = self.get_object(request, project_id)
        if project.position > 0:
            project.position -= 1
        project.save()
        return HttpResponseRedirectToReferrer(request)

    @admin.display(description=_("Actions"))
    def sort_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">&uarr;</a>&nbsp;<a class="button" href="{}">&darr;</a>',
            reverse("admin:project-up", args=[obj.pk]),
            reverse("admin:project-down", args=[obj.pk]),
        )


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "updated_at")
    search_fields = ("name", "is_active")


admin.site.register(Project, ProjectAdmin)
admin.site.register(SiteSetting, SiteSettingAdmin)
