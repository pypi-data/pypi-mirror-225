import logging
from django.core.management.base import BaseCommand
from app_ordering.models import Profile, AdminModel

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sort models in apps by alphabet"

    def handle(self, *args, **kwargs):  # noqa
        profile_qs = Profile.objects.prefetch_related("admin_apps__admin_models")
        for profile in profile_qs.all():
            for admin_app in profile.admin_apps.all():
                models = admin_app.admin_models.order_by('object_name')
                position = 1
                for model in models.all():
                    assert isinstance(model, AdminModel)
                    model.order = position
                    model.save()
                    position += 1
