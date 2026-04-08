from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import LandingPageView
from docs.views import hackathon_guidelines


urlpatterns = [
    path('', LandingPageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('contents/', include('contents.urls', namespace='contents')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('tags/', include('tags.urls', namespace='tags')),
    path('insights/', include('insights.urls', namespace='insights')),
    path('hackathon/', hackathon_guidelines, name='hackathon_guidelines'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
