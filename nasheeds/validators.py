import os

from django.core.exceptions import ValidationError

ALLOWED_AUDIO_TYPES = [
    "audio/mpeg",
    "audio/wav",
]

ALLOWED_EXTENSIONS = [
    ".mp3",
    ".wav",
]


def validate_audio(file):
    if file.size > 10 * 1024 * 1024:
        raise ValidationError("Audio size too large. Must be less than 10MB.")
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise ValidationError("File type not supported.")

    _, file_extension = os.path.splitext(file.name)
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError("File extension not supported.")
