from django.urls import path
from .views import *
from django.conf.urls import url 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('view_user/', ViewUserAPI.as_view(),name="user"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
#     path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('update_profile/<email>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('deleteuser/<email>/', DeleteUserView.as_view(),name='delete_user'),
    # path('profile_update_view/<email>',ProfileUpdateView.as_view(),name=''),
   path('rating_feedback/<email>/',UserRatingFeedbackView.as_view(),name='feedback'),
  

]
