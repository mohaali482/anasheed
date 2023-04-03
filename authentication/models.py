from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )
    image = models.ImageField(
        _("Image"), upload_to="users/images", blank=True, null=True
    )

    class Meta:
        verbose_name = _("userimage")
        verbose_name_plural = _("userimages")

    def __str__(self):
        return self.user.username
