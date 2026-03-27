from django.conf import settings
from django.db import models

from .validators import validate_file_extension, validate_file_size

CONTENT_TYPE_CHOICES = [
    ('article', 'Article'),
    ('video', 'Video'),
    ('podcast', 'Podcast'),
    ('course', 'Course'),
    ('book', 'Book'),
    ('tool', 'Tool'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]


class Content(models.Model):
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    preview_image_url = models.URLField(blank=True, max_length=500)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    file = models.FileField(
        upload_to='content_files/%Y/%m/',
        blank=True,
        null=True,
        validators=[validate_file_extension, validate_file_size],
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contents',
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contents',
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        blank=True,
        related_name='contents',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_card_image(self):
        """Returns the best available image URL for card display.

        Priority: uploaded image file > OG preview image > content type placeholder.
        """
        from django.templatetags.static import static

        # 1. Uploaded image file (if it's an image type)
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        try:
            if self.file:
                import os
                ext = os.path.splitext(self.file.name)[1].lower()
                if ext in image_extensions:
                    return self.file.url
        except Exception:
            pass

        # 2. Open Graph preview image
        if self.preview_image_url:
            return self.preview_image_url

        # 3. Content type placeholder SVG
        placeholder_map = {
            'article': 'images/placeholders/article.svg',
            'video': 'images/placeholders/video.svg',
            'podcast': 'images/placeholders/podcast.svg',
            'course': 'images/placeholders/course.svg',
            'book': 'images/placeholders/book.svg',
            'tool': 'images/placeholders/tool.svg',
            'other': 'images/placeholders/other.svg',
        }
        placeholder = placeholder_map.get(
            self.content_type, 'images/placeholders/other.svg'
        )
        return static(placeholder)
