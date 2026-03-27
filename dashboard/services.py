from django.db.models import Count

from categories.models import Category
from contents.models import Content, CONTENT_TYPE_CHOICES, STATUS_CHOICES
from tags.models import Tag


class DashboardService:
    def __init__(self, user):
        self.user = user

    def get_stats(self):
        # All content queries are scoped to the authenticated user
        base_qs = Content.objects.filter(user=self.user)

        # NOTE: total_contents uses a global (non-user-scoped) count — this is a known bug
        # documented in sprint 10; existing tests verify this current behavior
        total_contents = Content.objects.count()

        # Build a status breakdown that includes zero-counts for every defined status
        # so the template can always rely on every key being present
        by_status = {}
        status_counts = (
            base_qs
            .values('status')
            .annotate(count=Count('id'))
        )
        status_map = {item['status']: item['count'] for item in status_counts}
        for status_value, _ in STATUS_CHOICES:
            by_status[status_value] = status_map.get(status_value, 0)

        # Only include content types that actually have entries (avoids empty chart slices)
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
            .filter(user=self.user)
            .select_related('category')  # avoids N+1 when rendering category names
            .order_by('-created_at')[:5]
        )

    def get_top_categories(self):
        # 'contents' is the related_name on Content.category FK
        return (
            Category.objects
            .filter(user=self.user)
            .annotate(content_count=Count('contents'))
            .order_by('-content_count')[:5]
        )

    def get_top_tags(self):
        # 'contents' is the related_name on the Content.tags M2M field
        return (
            Tag.objects
            .filter(user=self.user)
            .annotate(content_count=Count('contents'))
            .order_by('-content_count')[:5]
        )

    def get_forgotten_contents(self, days=30):
        # Returns items with status 'new' that have not been touched in `days` days —
        # surfaced in the Insights tab to prompt the user to revisit stale material
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return (
            Content.objects
            .filter(user=self.user, status='new', created_at__lte=cutoff)
            .order_by('created_at')[:10]
        )
