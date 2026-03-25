from django.urls import path

from . import views

app_name = 'insights'

urlpatterns = [
    path('', views.InsightsIndexView.as_view(), name='index'),
    path('suggest-category/', views.SuggestCategoryView.as_view(), name='suggest_category'),
    path('generate-description/', views.GenerateDescriptionView.as_view(), name='generate_description'),
    path('generate-insights/', views.GenerateInsightsView.as_view(), name='generate_insights'),
]
