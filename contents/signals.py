from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Content
from .services import LinkPreviewService


@receiver(pre_save, sender=Content)
def fetch_preview_on_save(sender, instance, **kwargs):
    """Fetch OG preview image when content is created or URL changes."""
    if not instance.url:
        return

    # Skip if preview_image_url is already populated
    if instance.preview_image_url:
        return

    # On update: only fetch if URL has changed
    if instance.pk:
        try:
            old = Content.objects.get(pk=instance.pk)
            if old.url == instance.url:
                return
        except Content.DoesNotExist:
            pass

    # Fetch preview
    preview = LinkPreviewService().fetch_preview(instance.url)
    if preview and preview.get('preview_image_url'):
        instance.preview_image_url = preview['preview_image_url']
