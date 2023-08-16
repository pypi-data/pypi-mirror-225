from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group


class Profile(models.Model):
    created = models.DateTimeField(
        _("created"), default=now, blank=True, db_index=True, editable=False
    )
    name = models.CharField(_("name"), max_length=200, unique=True)
    is_default = models.BooleanField(_("is default"), default=False)
    users = models.ManyToManyField(User, verbose_name=_("users"), related_name="app_ordering_profile", blank=True)
    groups = models.ManyToManyField(Group, verbose_name=_("groups"), related_name="app_ordering_profile", blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.name)

    @property
    def next_app_order(self):
        max_admin_app = self.admin_apps.order_by('order').first()
        if not max_admin_app:
            return 1
        assert isinstance(max_admin_app, AdminApp)
        return max_admin_app.order + 1


class AdminApp(models.Model):
    created = models.DateTimeField(
        _("created"), default=now, blank=True, db_index=True, editable=False
    )
    app_label = models.CharField(_("app label"), max_length=200)
    order = models.PositiveIntegerField(_("order"), default=1, db_index=True)
    profile = models.ForeignKey(Profile, verbose_name=_("profile"), related_name="admin_apps", on_delete=models.CASCADE, )
    visible = models.BooleanField(_("visible"), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _("admin app")
        verbose_name_plural = _("admin apps")

    def __str__(self):
        return str(self.app_label)

    @property
    def next_model_order(self):
        max_admin_model = self.admin_models.order_by('order').first()
        if not max_admin_model:
            return 1
        assert isinstance(max_admin_model, AdminModel)
        return max_admin_model.order + 1


class AdminModel(models.Model):
    created = models.DateTimeField(
        _("created"), default=now, blank=True, db_index=True, editable=False
    )
    object_name = models.CharField(_("object name"), max_length=200)
    order = models.PositiveIntegerField(_("order"), default=1)
    admin_app = models.ForeignKey(AdminApp, verbose_name=_("admin app"), related_name='admin_models', on_delete=models.CASCADE, )
    visible = models.BooleanField(_("visible"), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _("admin model")
        verbose_name_plural = _("admin models")

    def __str__(self):
        return str(self.object_name)
