from django.urls import path

from . import views

app_name = 'contents'

urlpatterns = [
    path('', views.ContentListView.as_view(), name='list'),
    path('create/', views.ContentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ContentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ContentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ContentDeleteView.as_view(), name='delete'),
    path('<int:pk>/status/', views.ContentStatusUpdateView.as_view(), name='status_update'),
]
