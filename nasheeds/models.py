import mutagen
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
    duration = models.PositiveSmallIntegerField(_("Duration"), default=0)
    description = models.TextField(_("Description"), blank=True)
    # Future additions artists.
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("nasheed")
        verbose_name_plural = _("nasheeds")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        audio_info = mutagen.File(self.audio.file).info
        self.duration = audio_info.length

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("nasheed", kwargs={"pk": self.pk})


class SavedNasheed(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )
    nasheed = models.ForeignKey(
        "nasheeds.Nasheed", verbose_name=_("Nasheed"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("saved nasheed")
        verbose_name_plural = _("saved nasheeds")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "nasheed"], name="unique user and nasheed relation"
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.nasheed}"
