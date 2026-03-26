from django.urls import path

from . import views

app_name = 'insights'

urlpatterns = [
    path('', views.InsightsIndexView.as_view(), name='index'),
    path('suggest-category/', views.SuggestCategoryView.as_view(), name='suggest_category'),
    path('generate-description/', views.GenerateDescriptionView.as_view(), name='generate_description'),
    path('generate-insights/', views.GenerateInsightsView.as_view(), name='generate_insights'),
    path('suggest-next/', views.SuggestNextView.as_view(), name='suggest_next'),
    path('forgotten-contents/', views.ForgottenContentsView.as_view(), name='forgotten_contents'),
    path('analyze-topics/', views.AnalyzeTopicsView.as_view(), name='analyze_topics'),
    path('weekly-summary/', views.WeeklySummaryView.as_view(), name='weekly_summary'),
    path('chat/', views.ChatView.as_view(), name='chat'),
]
