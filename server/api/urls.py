from django.urls import path
from . import views
from .views import SignUpView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', views.Auth.as_view(), name='auth'),
    path('summoner/', views.RiotRegisterView.as_view(), name='summoner'),
    path('update/', views.UpdateView.as_view(), name='update'),
]
