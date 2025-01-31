from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _
from django_editorjs2.fields import EditorJSField


class Project(models.Model):
    class Meta:
        app_label = "core"
        db_table = "projects"
        default_permissions = ()
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("position",)

    def _upload_to_path(self, filename):
        return f"projects/{self.url_name}/{filename}"

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    url_name = models.SlugField(max_length=200)
    year = models.PositiveSmallIntegerField()

    text_top = EditorJSField(null=True)
    text_bottom_left = EditorJSField(null=True)
    text_bottom_right = EditorJSField(null=True)

    is_hidden = models.BooleanField(default=False)
    cover = models.ImageField(upload_to=_upload_to_path)
    position = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(db_default=Now())
    updated_at = models.DateTimeField(auto_now=True)


class ProjectImageRow(models.Model):
    class Meta:
        app_label = "core"
        db_table = "project_image_rows"
        default_permissions = ()
        verbose_name = _("Project image row")
        verbose_name_plural = _("Project image rows")
        ordering = ("position",)

    project = models.ForeignKey(Project, related_name="image_rows", on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(db_default=Now())

    def __str__(self):
        return f"Row in {self.project.title} (priority={self.position})"


class ProjectImage(models.Model):
    class Meta:
        app_label = "core"
        db_table = "project_images"
        default_permissions = ()
        verbose_name = _("Project image")
        verbose_name_plural = _("Project images")
        ordering = ("position",)

    def _upload_to_path(self, filename):
        return f"projects/{self.row.project.url_name}/{filename}"

    row = models.ForeignKey(ProjectImageRow, related_name="images", on_delete=models.CASCADE)
    content = models.ImageField(upload_to=_upload_to_path)
    mime = models.CharField(max_length=100)
    position = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(db_default=Now())
    updated_at = models.DateTimeField(auto_now=True)


class SiteSetting(models.Model):
    class Meta:
        app_label = "core"
        db_table = "site_settings"
        default_permissions = ()
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def _upload_to_path(self, filename):
        return f"intros/{filename}"

    name = models.CharField(max_length=100)
    site_description = models.TextField()
    site_keywords = models.TextField()
    intro_image = models.ImageField(upload_to=_upload_to_path)
    info_left = EditorJSField()
    info_right = EditorJSField()
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
