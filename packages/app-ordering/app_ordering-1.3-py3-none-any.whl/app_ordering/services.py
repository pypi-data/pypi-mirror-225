import logging

from django.apps import apps
from django.contrib import admin
from app_ordering.models import Profile, AdminApp, AdminModel
from typing import Optional


logger = logging.getLogger(__name__)


def sync_models(admin_app: AdminApp, all_model_object_names: list):
    active_model_name = []
    inactive_admin_model_ids = []
    for admin_model in admin_app.admin_models.all():
        assert isinstance(admin_model, AdminModel)
        if admin_model.object_name not in all_model_object_names:
            inactive_admin_model_ids.append(admin_model.pk)
        else:
            active_model_name.append(admin_model.object_name)
    next_order = admin_app.next_model_order
    for model_object_name in all_model_object_names:
        if model_object_name not in active_model_name:
            admin_model = AdminModel(admin_app=admin_app, object_name=model_object_name, order=next_order)
            admin_model.save()
            next_order += 1
    if len(inactive_admin_model_ids) > 0:
        AdminModel.objects.filter(pk__in=inactive_admin_model_ids).delete()


def sync_apps(profile_id: Optional[int] = None):
    models = apps.get_models()
    map_app = {}
    all_apps = []
    for model in models:
        if model in admin.site._registry:  # pylint: disable=protected-access
            app_label = model._meta.app_label
            object_name = model._meta.object_name
            if app_label not in map_app:
                map_app[app_label] = []
                all_apps.append(app_label)
            if object_name not in map_app[app_label]:
                map_app[app_label].append(object_name)
                
    all_apps = sorted(all_apps)
    
    for app_label in map_app:
        map_app[app_label] = sorted(map_app[app_label])

    profile_qs = Profile.objects.prefetch_related("admin_apps__admin_models")
    if profile_id:
        profile_qs.filter(pk=profile_id)

    for profile in profile_qs.all():
        active_app_labels = []
        inactive_app_ids = []
        for admin_app in profile.admin_apps.all():
            assert isinstance(admin_app, AdminApp)
            if admin_app.app_label not in map_app:
                inactive_app_ids.append(admin_app.pk)
            else:
                active_app_labels.append(admin_app.app_label)
                sync_models(admin_app, map_app[admin_app.app_label])
        next_order = profile.next_app_order
        for app_label in all_apps:
            if app_label not in active_app_labels:
                admin_app = AdminApp(profile=profile, app_label=app_label, order=next_order)
                admin_app.save()
                next_order += 1
                sync_models(admin_app, map_app[admin_app.app_label])
                logger.info('new app %s', admin_app)
        if len(inactive_app_ids) > 0:
            logger.info('Removed inactive apps %s', inactive_app_ids)
            AdminApp.objects.filter(pk__in=inactive_app_ids).delete()