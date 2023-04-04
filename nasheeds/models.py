from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .validators import validate_audio


class Nasheed(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Owner"), on_delete=models.CASCADE
    )
    name = models.CharField(_("Name"), max_length=255)
    poster = models.ImageField(_("Poster"), upload_to="nasheeds/posters")
    audio = models.FileField(
        _("Audio"),
        upload_to="nasheeds/audios",
        validators=[validate_audio],
    )
    # Future additions artists.
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("nasheed")
        verbose_name_plural = _("nasheeds")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nasheed", kwargs={"pk": self.pk})
