from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from djangoldp.admin import DjangoLDPAdmin

from .models import (
    Application,
    ApplicationComponent,
    ApplicationComponentParameter,
    ApplicationGraphics,
    ApplicationNPM,
    ApplicationPackage,
    ApplicationPackageParameter,
    ApplicationService,
    ComponentExtension,
    ComponentExtensionParameter,
    Deployment,
    Federation,
)


@admin.register(ApplicationComponentParameter, ApplicationGraphics, ApplicationNPM, ApplicationPackageParameter, ApplicationService, ComponentExtensionParameter, Federation)
class EmptyAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class ApplicationComponentInline(admin.TabularInline):
    model = ApplicationComponent
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    fields = ("component",)
    show_change_link = True
    extra = 0


class ApplicationServiceInline(admin.TabularInline):
    model = ApplicationService
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    fields = ("primary_key", "key", "value")
    extra = 0


class ApplicationGraphicsInline(admin.TabularInline):
    model = ApplicationGraphics
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    fields = ("primary_key", "key", "value")
    extra = 0


class ApplicationNPMInline(admin.TabularInline):
    model = ApplicationNPM
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    fields = ("package", "version")
    extra = 0


class ApplicationPackageInline(admin.TabularInline):
    model = ApplicationPackage
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    fields = ("package",)
    show_change_link = True
    extra = 0


class FederationInline(admin.TabularInline):
    model = Federation
    fk_name = "application"
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(Application)
class ApplicationAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "friendly_name", "short_description")
    exclude = (
        "urlid",
        "slug",
        "is_backlink",
        "allow_create_backlink",
    )
    inlines = [
        ApplicationGraphicsInline,
        ApplicationServiceInline,
        ApplicationNPMInline,
        ApplicationComponentInline,
        ApplicationPackageInline,
        FederationInline,
    ]
    search_fields = ["urlid", "friendly_name", "short_description"]
    ordering = ["slug"]


class ApplicationPackageParameterInline(admin.TabularInline):
    model = ApplicationPackageParameter
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(ApplicationPackage)
class ApplicationPackageAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "application", "package")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    inlines = [ApplicationPackageParameterInline]
    search_fields = [
        "urlid",
        "package__friendly_name",
        "package__short_description",
        "application__friendly_name",
        "application__short_description",
    ]
    ordering = ["application__slug", "package__slug"]


class ApplicationComponentParameterInline(admin.TabularInline):
    model = ApplicationComponentParameter
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(ApplicationComponent)
class ApplicationComponentAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "application", "component")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    inlines = [ApplicationComponentParameterInline]
    search_fields = [
        "urlid",
        "component__friendly_name",
        "component__short_description",
        "application__friendly_name",
        "application__short_description",
    ]
    ordering = ["application__slug", "component__slug"]


class ComponentExtensionParameterInline(admin.TabularInline):
    model = ComponentExtensionParameter
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(ComponentExtension)
class ComponentExtensionAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "base_component", "component")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    inlines = [ComponentExtensionParameterInline]
    search_fields = [
        "urlid",
        "component__friendly_name",
        "component__short_description",
        "base_component__component__friendly_name",
        "base_component__component__short_description",
        "base_component__application__friendly_name",
        "base_component__application__short_description",
    ]
    ordering = ["base_component__application__slug", "component__slug"]


@admin.register(Deployment)
class DeploymentAdmin(DjangoLDPAdmin):
    list_display = ("application", "requester", "date", "status", "resolutionDate")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    search_fields = [
        "urlid",
        "application__slug",
        "requester__name",
        "application__friendly_name",
    ]
    ordering = ["application__slug", "date", "resolutionDate"]


