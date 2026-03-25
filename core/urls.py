from django.contrib import admin
from django.urls import include, path

from core.views import LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('contents/', include('contents.urls', namespace='contents')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('tags/', include('tags.urls', namespace='tags')),
    path('insights/', include('insights.urls', namespace='insights')),
]
