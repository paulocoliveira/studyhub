from django.urls import path

from tags.views import TagListView

app_name = 'tags'

urlpatterns = [
    path('', TagListView.as_view(), name='list'),
]
