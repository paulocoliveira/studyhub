from django.urls import path

from insights.views import InsightsIndexView

app_name = 'insights'

urlpatterns = [
    path('', InsightsIndexView.as_view(), name='index'),
]
