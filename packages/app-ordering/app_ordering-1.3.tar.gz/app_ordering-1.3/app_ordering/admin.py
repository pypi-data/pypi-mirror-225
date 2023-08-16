from typing import Optional, Any
from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from app_ordering.services import sync_apps
from django.contrib.messages import add_message, SUCCESS
from adminsortable2.admin import SortableTabularInline
from adminsortable2.admin import SortableAdminBase

from app_ordering.models import Profile, AdminApp, AdminModel


class AdminAppInlineAdmin(SortableTabularInline):
    model = AdminApp
    readonly_fields = (
        "edit_link",
        "app_label",
    )
    extra = 0

    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False

    def edit_link(self, instance):
        url = reverse(
            "admin:%s_%s_change" % (instance._meta.app_label, instance._meta.model_name),
            args=[instance.pk],
        )
        if instance.pk:
            return mark_safe('<a href="{u}">edit</a>'.format(u=url))
        else:
            return ""


class AdminModelInlineAdmin(SortableTabularInline):
    model = AdminModel
    extra = 0
    readonly_fields = ('object_name', )

    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False


class ProfileAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["created", "name", "is_default"]
    autocomplete_fields = ('users', 'groups')
    inlines = [
        AdminAppInlineAdmin,
    ]

    def changelist_view(self, request, extra_context=None):  # pylint: disable=too-many-locals
        sync_app = request.POST.get("sync_app")
        if sync_app:
            sync_apps()
            add_message(request, SUCCESS, _("all apps are synched"))  # noqa

        return super().changelist_view(request, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        sync_apps(obj.pk)
        return super().response_add(request, obj, post_url_continue)


class AdminAppAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = [
        "created",
        "app_label",
    ]
    inlines = [
        AdminModelInlineAdmin,
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_delete'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(AdminApp, AdminAppAdmin)
