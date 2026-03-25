from django.urls import path

from users.views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    RegisterView,
    UserSettingsView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
]
