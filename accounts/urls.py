from django.urls import path
from accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, UserView
from django.urls import path



urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', UserView.as_view(), name='users'),

]   