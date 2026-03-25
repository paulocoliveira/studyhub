from django.urls import path

from contents.views import ContentListView

app_name = 'contents'

urlpatterns = [
    path('', ContentListView.as_view(), name='list'),
]
