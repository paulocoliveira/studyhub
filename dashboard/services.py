from django.db.models import Count

from categories.models import Category
from contents.models import Content, CONTENT_TYPE_CHOICES, STATUS_CHOICES
from tags.models import Tag


class DashboardService:
    def __init__(self, user):
        self.user = user

    def get_stats(self):
        base_qs = Content.objects.filter(user=self.user)

        total_contents = base_qs.count()

        by_status = {}
        status_counts = (
            base_qs
            .values('status')
            .annotate(count=Count('id'))
        )
        status_map = {item['status']: item['count'] for item in status_counts}
        for status_value, _ in STATUS_CHOICES:
            by_status[status_value] = status_map.get(status_value, 0)

        by_type = list(
            base_qs
            .values('content_type')
            .annotate(count=Count('id'))
            .filter(count__gt=0)
            .order_by('-count')
        )

        return {
            'total_contents': total_contents,
            'by_status': by_status,
            'by_type': by_type,
        }

    def get_recent_added(self):
        return (
            Content.objects
            .filter(user=self.user)
            .order_by('-created_at')[:5]
        )

    def get_recent_completed(self):
        return (
            Content.objects
            .filter(user=self.user, status='completed')
            .order_by('-updated_at')[:5]
        )

    def get_top_categories(self):
        return (
            Category.objects
            .filter(user=self.user)
            .annotate(content_count=Count('contents'))
            .order_by('-content_count')[:5]
        )

    def get_top_tags(self):
        return (
            Tag.objects
            .filter(user=self.user)
            .annotate(content_count=Count('contents'))
            .order_by('-content_count')[:5]
        )

    def get_forgotten_contents(self, days=30):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return (
            Content.objects
            .filter(user=self.user, status='new', created_at__lte=cutoff)
            .order_by('created_at')[:10]
        )
