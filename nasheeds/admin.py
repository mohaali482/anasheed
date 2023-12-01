from django.contrib import admin

from .models import Nasheed, SavedNasheed


@admin.register(Nasheed)
class NasheedAdmin(admin.ModelAdmin):
    pass


@admin.register(SavedNasheed)
class SavedNasheedAdmin(admin.ModelAdmin):
    pass
