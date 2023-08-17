from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template import loader
from django.utils.translation import gettext_lazy as _
from djangoldp.filters import LocalObjectOnContainerPathBackend
from djangoldp.models import Model
from djangoldp.views import LDPViewSet
from djangoldp_application.models import (
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
    Federation,
)
from djangoldp_component.models import Component, Package
from rest_framework import response, serializers, status, viewsets
from rest_framework_yaml.parsers import YAMLParser
from rest_framework_yaml.renderers import YAMLRenderer

EMAIL_FROM = getattr(settings, "DEFAULT_FROM_EMAIL", False) or getattr(
    settings, "EMAIL_HOST_USER", False
)
ANSIBLE_SERVERS = set({"127.0.0.1"})


if hasattr(settings, "ANSIBLE_SERVERS"):
    ANSIBLE_SERVERS = ANSIBLE_SERVERS.union(getattr(settings, "ANSIBLE_SERVERS"))


def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def format(value):
    if not value == str(value):
        return ""
    v = value.lower()
    if v == "false":
        return False
    elif v == "true":
        return True
    else:
        return value.replace("\r\n", "\n").replace("\n\n", "\n")


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ("slug", "deploy")


class ApplicationDetailSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, obj):
        application = super().to_representation(obj)

        federation = []
        for host in application["federation"]:
            federation.append(Federation.objects.get(urlid=host).target.api_url)

        serialized = {"apps": {"hosts": {}}}
        serialized["apps"]["hosts"][application["slug"]] = {
            "graphics": {},
            "data": {"api": application["api_url"], "with": federation},
            "packages": [],
            "components": [],
        }

        if application["client_url"]:
            serialized["apps"]["hosts"][application["slug"]]["graphics"][
                "client"
            ] = application["client_url"]

        if application["repository"]:
            serialized["apps"]["hosts"][application["slug"]]["graphics"][
                "canva"
            ] = application["repository"]

        if application["application_title"]:
            serialized["apps"]["hosts"][application["slug"]]["graphics"][
                "title"
            ] = application["application_title"]

        if application["application_logo"]:
            serialized["apps"]["hosts"][application["slug"]]["graphics"][
                "logo"
            ] = application["application_logo"]

        if len(application["graphics"]) > 0:
            for applicationGraphic in application["graphics"]:
                if applicationGraphic.obj.primary_key:
                    if (
                        applicationGraphic.obj.primary_key
                        not in serialized["apps"]["hosts"][application["slug"]][
                            "graphics"
                        ]
                    ):
                        serialized["apps"]["hosts"][application["slug"]]["graphics"][
                            applicationGraphic.obj.primary_key
                        ] = {}
                    serialized["apps"]["hosts"][application["slug"]]["graphics"][
                        applicationGraphic.obj.primary_key
                    ][applicationGraphic.obj.key] = format(applicationGraphic.obj.value)
                else:
                    serialized["apps"]["hosts"][application["slug"]]["graphics"][
                        applicationGraphic.obj.key
                    ] = format(applicationGraphic.obj.value)

        if len(application["services"]) > 0:
            serialized["apps"]["hosts"][application["slug"]]["services"] = {}
            for applicationService in application["services"]:
                if applicationService.obj.primary_key:
                    if (
                        applicationService.obj.primary_key
                        not in serialized["apps"]["hosts"][application["slug"]][
                            "services"
                        ]
                    ):
                        serialized["apps"]["hosts"][application["slug"]]["services"][
                            applicationService.obj.primary_key
                        ] = {}
                    serialized["apps"]["hosts"][application["slug"]]["services"][
                        applicationService.obj.primary_key
                    ][applicationService.obj.key] = format(applicationService.obj.value)
                else:
                    serialized["apps"]["hosts"][application["slug"]]["services"][
                        applicationService.obj.key
                    ] = format(applicationService.obj.value)

        if len(application["npms"]) > 0:
            serialized["apps"]["hosts"][application["slug"]]["npm"] = []
            for applicationNPM in application["npms"]:
                serialized["apps"]["hosts"][application["slug"]]["npm"].append(
                    {
                        "package": applicationNPM.obj.package,
                        "version": applicationNPM.obj.version,
                    }
                )

        for applicationComponent in application["components"]:
            component = Component.objects.get(id=applicationComponent.obj.component_id)
            insertComponent = {
                "type": component.name,
                "route": format(component.preferred_route),
                "parameters": {},
                "extensions": [],
                "experimental": [],
            }
            if component.auto_import:
                insertComponent["experimental"].append("routing")
            if component.auto_menu:
                insertComponent["experimental"].append("menu")
            keys = []
            for parameter in applicationComponent.obj.parameters.all():
                if parameter.key == "route":
                    insertComponent["route"] = format(parameter.value)
                    keys.append(parameter.key)
                elif parameter.key == "defaultRoute":
                    insertComponent["defaultRoute"] = format(parameter.value)
                    keys.append(parameter.key)
                elif not parameter.key in keys:
                    insertComponent["parameters"][parameter.key] = format(
                        parameter.value
                    )
                    keys.append(parameter.key)
                elif hasattr(
                    insertComponent["parameters"][parameter.key], "__len__"
                ) and (
                    not isinstance(insertComponent["parameters"][parameter.key], str)
                ):
                    insertComponent["parameters"][parameter.key].append(
                        format(parameter.value)
                    )
                else:
                    insertComponent["parameters"][parameter.key] = [
                        insertComponent["parameters"][parameter.key],
                        format(parameter.value),
                    ]

            if component.script_tags.all().count() > 0:
                if(not "npm" in serialized["apps"]["hosts"][application["slug"]]):
                    serialized["apps"]["hosts"][application["slug"]]["npm"] = []

                for script_tag in component.script_tags.all():
                    serialized["apps"]["hosts"][application["slug"]]["npm"].append(
                        {
                            "version": "0",
                            "path": script_tag.src,
                        }
                    )

            missingKeys = []
            for parameter in component.parameters.all():
                if not parameter.key in keys:
                    if parameter.key == "route":
                        insertComponent["route"] = format(parameter.default)
                        missingKeys.append(parameter.key)
                    elif parameter.key == "defaultRoute":
                        insertComponent["defaultRoute"] = format(parameter.default)
                        keys.append(parameter.key)
                    elif not parameter.key in missingKeys:
                        insertComponent["parameters"][parameter.key] = format(
                            parameter.default
                        )
                        missingKeys.append(parameter.key)
                    elif hasattr(
                        insertComponent["parameters"][parameter.key], "__len__"
                    ) and (
                        not isinstance(
                            insertComponent["parameters"][parameter.key], str
                        )
                    ):
                        insertComponent["parameters"][parameter.key].append(
                            format(parameter.default)
                        )
                    else:
                        insertComponent["parameters"][parameter.key] = [
                            insertComponent["parameters"][parameter.key],
                            format(parameter.default),
                        ]
            for extensionComponent in applicationComponent.obj.extensions.all():
                extension = Component.objects.get(id=extensionComponent.component_id)
                componentExtension = {
                    "type": extension.name,
                    "route": format(component.preferred_route),
                    "parameters": {},
                    "experimental": [],
                }
                if component.auto_import:
                    insertComponent["experimental"].append("routing")
                if component.auto_menu:
                    insertComponent["experimental"].append("menu")
                keys = []
                for parameter in extensionComponent.parameters.all():
                    if parameter.key == "route":
                        componentExtension["route"] = format(parameter.value)
                        keys.append(parameter.key)
                    elif parameter.key == "defaultRoute":
                        componentExtension["defaultRoute"] = format(parameter.value)
                        keys.append(parameter.key)
                    elif not parameter.key in keys:
                        componentExtension["parameters"][parameter.key] = format(
                            parameter.value
                        )
                        keys.append(parameter.key)
                    elif hasattr(
                        insertComponent["parameters"][parameter.key], "__len__"
                    ) and (
                        not isinstance(
                            componentExtension["parameters"][parameter.key], str
                        )
                    ):
                        componentExtension["parameters"][parameter.key].append(
                            format(parameter.value)
                        )
                    else:
                        componentExtension["parameters"][parameter.key] = [
                            componentExtension["parameters"][parameter.key],
                            format(parameter.value),
                        ]
                missingKeys = []
                for parameter in extension.parameters.all():
                    if not parameter.key in keys:
                        if parameter.key == "route":
                            componentExtension["route"] = format(parameter.default)
                            missingKeys.append(parameter.key)
                        elif parameter.key == "defaultRoute":
                            componentExtension["defaultRoute"] = format(
                                parameter.default
                            )
                            missingKeys.append(parameter.key)
                        elif not parameter.key in missingKeys:
                            componentExtension["parameters"][parameter.key] = format(
                                parameter.default
                            )
                            missingKeys.append(parameter.key)
                        elif hasattr(
                            componentExtension["parameters"][parameter.key], "__len__"
                        ) and (
                            not isinstance(
                                componentExtension["parameters"][parameter.key], str
                            )
                        ):
                            componentExtension["parameters"][parameter.key].append(
                                format(parameter.default)
                            )
                        else:
                            componentExtension["parameters"][parameter.key] = [
                                componentExtension["parameters"][parameter.key],
                                format(parameter.default),
                            ]
                insertComponent["extensions"].append(componentExtension)
            serialized["apps"]["hosts"][application["slug"]]["components"].append(
                insertComponent
            )

        insertDependencies = []
        for applicationPackage in application["packages"]:
            package = Package.objects.get(id=applicationPackage.obj.package_id)
            insertDependency = {
                "distribution": package.distribution,
                "module": package.module,
                "parameters": {},
            }
            keys = []
            for parameter in applicationPackage.obj.parameters.all():
                if not parameter.key in keys:
                    insertDependency["parameters"][parameter.key] = format(
                        parameter.value
                    )
                    keys.append(parameter.key)
                elif hasattr(
                    insertDependency["parameters"][parameter.key], "__len__"
                ) and (
                    not isinstance(insertDependency["parameters"][parameter.key], str)
                ):
                    insertDependency["parameters"][parameter.key].append(
                        format(parameter.value)
                    )
                else:
                    insertDependency["parameters"][parameter.key] = [
                        insertDependency["parameters"][parameter.key],
                        format(parameter.value),
                    ]
            missingKeys = []
            for parameter in package.parameters.all():
                if not parameter.key in keys:
                    if not parameter.key in missingKeys:
                        insertDependency["parameters"][parameter.key] = format(
                            parameter.default
                        )
                        missingKeys.append(parameter.key)
                    elif hasattr(
                        insertDependency["parameters"][parameter.key], "__len__"
                    ) and (
                        not isinstance(
                            insertDependency["parameters"][parameter.key], str
                        )
                    ):
                        insertDependency["parameters"][parameter.key].append(
                            format(parameter.default)
                        )
                    else:
                        insertDependency["parameters"][parameter.key] = [
                            insertDependency["parameters"][parameter.key],
                            format(parameter.default),
                        ]
            insertDependencies.append(insertDependency)
        serialized["apps"]["hosts"][application["slug"]][
            "packages"
        ] = insertDependencies

        return serialized

    class Meta:
        model = Application
        lookup_field = "slug"
        fields = [
            "urlid",
            "slug",
            "api_url",
            "client_url",
            "application_title",
            "application_logo",
            "services",
            "graphics",
            "npms",
            "components",
            "packages",
            "repository",
            "federation",
        ]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)


class ApplicationDetailViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer
    lookup_field = "slug"
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)


class CreateApplicationViewSet(LDPViewSet):
    model = Application
    depth = 0

    def __init__(self, **kwargs):
        viewsets.ModelViewSet.__init__(self, **kwargs)
        if self.permission_classes:
            filtered_classes = [
                p
                for p in self.permission_classes
                if hasattr(p, "filter_backends") and p.filter_backends is not None
            ]
            for p in filtered_classes:
                self.filter_backends = list(
                    set(self.filter_backends).union(set(p.filter_backends))
                )

        if getattr(settings, "DISABLE_LOCAL_OBJECT_FILTER", False):
            if LocalObjectOnContainerPathBackend in self.filter_backends:
                self.filter_backends.remove(LocalObjectOnContainerPathBackend)

        self.serializer_class = self.build_read_serializer()
        self.write_serializer_class = self.build_write_serializer()

    def create(self, request, *args, **kwargs):
        self.check_model_permissions(request)
        serializer = self.get_write_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.is_safe_create(request.user, serializer.validated_data):
            return response.Response(
                {"detail": "You do not have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        entry = self.perform_create(serializer)

        if serializer.initial_data["source"]:
            container, source_application = Model.resolve(
                serializer.initial_data["source"]["@id"]
            )

            try:
                for component_relation in source_application.components.all():
                    (
                        new_component_relation,
                        created,
                    ) = ApplicationComponent.objects.get_or_create(
                        component=component_relation.component, application=entry
                    )
                    for parameter in component_relation.parameters.all():
                        ApplicationComponentParameter.objects.create(
                            component=new_component_relation,
                            key=parameter.key,
                            value=parameter.value,
                        )
                    for extension in component_relation.extensions.all():
                        (
                            new_extension_relation,
                            created,
                        ) = ComponentExtension.objects.get_or_create(
                            base_component=new_component_relation,
                            component=extension.component,
                        )
                        for parameter in new_extension_relation.parameters.all():
                            ComponentExtensionParameter.objects.create(
                                component=new_extension_relation,
                                key=parameter.key,
                                value=parameter.value,
                            )
            except:
                pass

            try:
                for package_relation in source_application.packages.all():
                    (
                        new_package_relation,
                        created,
                    ) = ApplicationPackage.objects.get_or_create(
                        package=package_relation.package, application=entry
                    )
                    for parameter in package_relation.parameters.all():
                        ApplicationPackageParameter.objects.create(
                            package=new_package_relation,
                            key=parameter.key,
                            value=parameter.value,
                        )
            except:
                pass

            try:
                for application_npm in source_application.npms.all():
                    ApplicationNPM.objects.get_or_create(
                        application=entry,
                        package=application_npm.package,
                        version=application_npm.version,
                    )
            except:
                pass

            try:
                for application_service in source_application.services.all():
                    ApplicationService.objects.get_or_create(
                        application=entry,
                        primary_key=application_service.primary_key,
                        key=application_service.key,
                        value=application_service.value,
                    )
            except:
                pass

            try:
                for application_graphic in source_application.graphics.all():
                    ApplicationGraphics.objects.get_or_create(
                        application=entry,
                        primary_key=application_graphic.primary_key,
                        key=application_graphic.key,
                        value=application_graphic.value,
                    )
            except:
                pass

            try:
                for application_federation in source_application.federation.all():
                    Federation.objects.get_or_create(
                        application=entry, target=application_federation.target
                    )
            except:
                pass

        response_serializer = self.get_serializer()
        container, updated_entry = Model.resolve(serializer.instance.urlid)
        data = response_serializer.to_representation(updated_entry)
        headers = self.get_success_headers(data)
        return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)


def mark_as_doing(request, slug):
    if request.method == "GET" and get_client_ip(request) in ANSIBLE_SERVERS:
        application = Application.objects.get(slug=slug)
        for deploy in application.deployments.filter(status="Todo"):
            deploy.status = "Doing"
            deploy.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "invalid request"}, status=400)


def mark_as_done(request, slug):
    if request.method == "GET" and get_client_ip(request) in ANSIBLE_SERVERS:
        application = Application.objects.get(slug=slug)
        for deploy in application.deployments.filter(status="Doing"):
            deploy.status = "Done"
            deploy.save()

            if deploy.requester:
                requester = deploy.requester
            else:
                requester = application.creator

            if application.deployments.count() == 1:
                html_message = loader.render_to_string(
                    "djangoldp_application/email.html",
                    {
                        "message": _("Deployment done. You can use the default account: admin/admin. Don't forget to create your own account."),
                        "link": application.client_url,
                        "object": "{} https://{}".format(
                            _("About your deployment of"), application.client_url
                        ),
                    },
                )
            else :
                html_message = loader.render_to_string(
                    "djangoldp_application/email.html",
                    {
                        "message": _("Deployment done."),
                        "link": application.client_url,
                        "object": "{} https://{}".format(
                            _("About your deployment of"), application.client_url
                        ),
                    },
                )

            send_mail(
                "{} (https://{})".format(
                    _("Déploiement de ") + application.application_title,
                    application.client_url,
                ),
                _("Deployment done"),
                EMAIL_FROM,
                [requester.email],
                fail_silently=True,
                html_message=html_message,
            )

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "invalid request"}, status=400)


def mark_as_failed(request, slug):
    if request.method == "GET" and get_client_ip(request) in ANSIBLE_SERVERS:
        application = Application.objects.get(slug=slug)
        for deploy in application.deployments.filter(status="Doing"):
            deploy.status = "Failed"
            deploy.save()
            if deploy.requester:
                html_message = loader.render_to_string(
                    "djangoldp_application/email.html",
                    {
                        "message": _("Deployment failed"),
                        "link": (getattr(settings, 'INSTANCE_DEFAULT_CLIENT', False) or getattr(settings, 'JABBER_DEFAULT_HOST')),
                        "object": "{} https://{}".format(
                            _("About your deployment of"), application.client_url
                        ),
                    },
                )

                send_mail(
                    "{} (https://{})".format(
                        _("Déploiement de ") + application.application_title,
                        application.client_url,
                    ),
                    _("Deployment failed"),
                    EMAIL_FROM,
                    [deploy.requester.email],
                    fail_silently=True,
                    html_message=html_message,
                )

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "invalid request"}, status=400)
