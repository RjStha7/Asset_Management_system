from django.urls import path
from accounts.views import ChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, UserProfileView, UserRegistrationView, UserLoginView, UserLogoutView, UserView, admin_verify, api_overview




urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', UserView.as_view(), name='users'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name = 'send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name = 'reset-password'),
    path('user-profile/', UserProfileView.as_view(), name = "user-profile"),
    path('admin-verify/', admin_verify, name='admin-verify'),
    path('api-overview/', api_overview, name='api-overview')
]