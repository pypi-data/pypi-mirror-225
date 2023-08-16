from django.apps import AppConfig
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

APP_NAME = "app_ordering"


class AppOrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP_NAME
    verbose_name = _("App ordering")

    def ready(self):
        def get_app_list(self, request, app_label=None):
            from app_ordering.models import Profile, AdminApp
            from django.contrib.auth.models import User

            user = request.user
            selected_profile = None
            app_dict = self._build_app_dict(request, app_label)

            if isinstance(user, User):

                user_groups = user.groups.all()

                if len(user_groups) > 0:
                    selected_profile_qs = Profile.objects.filter(Q(groups__in=user_groups) | Q(users__in=[user]))
                else:
                    selected_profile_qs = Profile.objects.filter(users__in=[user])

                selected_profile = selected_profile_qs.prefetch_related("admin_apps__admin_models").first()
                if not selected_profile:  # Pick by default profile
                    selected_profile = (
                        Profile.objects.filter(is_default=True)
                        .prefetch_related("admin_apps__admin_models")
                        .first()
                    )
            if not selected_profile:
                app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())  # Sort the apps alphabetically.

                # Sort the models alphabetically within each app.
                for app in app_list:
                    app["models"].sort(key=lambda x: x["name"])
                    app["visible"] = True
                    for model in app["models"]:
                        model["visible"] = True

                return app_list

            m_app_orders = {}

            for admin_app in selected_profile.admin_apps.all():
                assert isinstance(admin_app, AdminApp)
                m_app_orders[admin_app.app_label] = {
                    "order": admin_app.order,
                    "visible": admin_app.visible or admin_app.app_label == APP_NAME,  # Ignore itself
                    "modules": {},
                }

                all_module_invisible = True
                for admin_model in admin_app.admin_models.all():

                    module_visible = admin_model.visible or admin_app.app_label == APP_NAME
                    if module_visible and all_module_invisible:
                        all_module_invisible = False

                    m_app_orders[admin_app.app_label]["modules"][admin_model.object_name] = {
                        "order": admin_model.order,
                        "visible": module_visible,  # Ignore itself
                    }
                if all_module_invisible:
                    m_app_orders[admin_app.app_label]['visible'] = False

            app_list = sorted(
                app_dict.values(),
                key=lambda x: (
                    1000
                    if x["app_label"] not in m_app_orders
                    else m_app_orders[x["app_label"]]["order"],
                    x["name"].lower(),
                ),
            )

            for app in app_list:
                app["visible"] = (
                    app["app_label"] not in m_app_orders
                    or m_app_orders[app["app_label"]]["visible"]
                )

                app_modules = m_app_orders.get(app["app_label"], {}).get("modules", {})
                app["models"].sort(
                    key=lambda x: (
                        1000
                        if x["object_name"] not in app_modules
                        else app_modules[x["object_name"]]["order"],
                        x["name"],
                    )
                )
                for model in app["models"]:
                    model['visible'] = True if model["object_name"] not in app_modules else app_modules[model["object_name"]]['visible']

            return app_list

        admin.AdminSite.get_app_list = get_app_list

        from . import signals as signals_init  # noqa
