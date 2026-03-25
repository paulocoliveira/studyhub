import os

from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = {
    '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp',
    '.mp3', '.mp4', '.doc', '.docx', '.txt', '.md',
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        allowed = ', '.join(sorted(ALLOWED_EXTENSIONS))
        raise ValidationError(
            f'File type "{ext}" is not allowed. Allowed formats: {allowed}'
        )


def validate_file_size(value):
    if value.size > MAX_FILE_SIZE:
        size_mb = value.size / (1024 * 1024)
        raise ValidationError(
            f'File size must not exceed 10MB. Current size: {size_mb:.1f} MB'
        )
