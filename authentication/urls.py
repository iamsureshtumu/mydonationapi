from django.urls import path, include
from .views import *
from authentication import views
# from django.conf.urls import url 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('01/register/', RegisterView.as_view(), name="register"),
    path('03/login/', LoginAPIView.as_view(), name="login"),
    path('12/logout/', LogoutAPIView.as_view(), name="logout"),
    path('04/view_user/', ViewUserAPI.as_view(),name="user"),
    path('02/email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('10/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('06/request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('07/password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('08/password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('05/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('09/update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    # path('update_profile/<email>/', UpdateProfileView.as_view(), name='auth_update_profile'),

    # path('deleteuser/<email>/', DeleteUserView.as_view(),name='delete_user'),
    path('11/deleteuser/', DeleteUserView.as_view(),name='delete_user'),

    # path('profile_update_view/<email>',ProfileUpdateView.as_view(),name=''),

    # path('User/rating_feedback/',userRatingFeedbackView.as_view(),name='feedback'),
    
    # path('rating_feedback/<email>/',UserRatingFeedbackView.as_view(),name='feedback'),

    path('13/feedback_rating/',AnonymousRatingFeedbackView.as_view()),
    # path('list/', CreateView.as_view(),name='view'),
    # path('dlist/',DetailsView.as_view(),name='dview'),

    path('14/guestuser_orderID/',GuestUserApiView.as_view(),name='guestuserorderid'),
    path('15/guestuser_Transaction_Successful/<secret_key>/', TransactionSuccessfulAPIView.as_view(), name='transactiontoken'),

    path('16/user_orderID/',UserTxnApiView.as_view(),name='userorderid'),
    path('17/user_Transaction_Successful/<referrence_number>/', UserTxnSuccessfulAPIView.as_view(), name='usertransactiontoken'),

    path('18/AdminView_GuestUser/<email>/',AdminViewGuestUserAPI.as_view(),name='adminviewguestuser'),
    path('19/AdminView_User/<email>/',AdminViewUserAPI.as_view(),name='adminviewuser'), 
    path('20/No_Of_Transactions_by_user/<user_id>/',NoOfTransactions.as_view(),name='nooftransactions'),
]
