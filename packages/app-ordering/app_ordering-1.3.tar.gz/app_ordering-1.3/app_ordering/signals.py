from django.db.models.signals import post_save
from app_ordering.models import Profile
from django.dispatch import receiver


@receiver(post_save, sender=Profile)
def profile_post_save(sender, instance, created, **kwargs):
    assert isinstance(instance, Profile)
    if instance.is_default:
        Profile.objects.exclude(pk=instance.pk).update(is_default=False)
