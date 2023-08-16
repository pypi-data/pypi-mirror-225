import logging
from django.core.management.base import BaseCommand
from app_ordering.services import sync_apps

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Scan all apps, models in the system and sync to Admin menu"

    def handle(self, *args, **kwargs):  # noqa
        sync_apps()
