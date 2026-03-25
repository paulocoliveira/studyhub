from django.contrib import admin

from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'status', 'user', 'category', 'created_at']
    list_filter = ['status', 'content_type', 'user']
    search_fields = ['title', 'description', 'url']
