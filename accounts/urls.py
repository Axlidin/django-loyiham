from django.urls import path
from .views import profile_page_view, signup_view, sigUpView, UserRegisterCreatView, ProfileEditView, admin_page_view
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

app_name = 'accounts'

urlpatterns = [
    # path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('signup/', signup_view, name='sigup'),#function base view
    path('signup/', sigUpView.as_view(), name='signup'),#oddiy view
    # path('signup/', UserRegisterCreatView.as_view(), name='sigup'),#generic view

    path('profile/', profile_page_view, name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),


    path('adminpage/', admin_page_view, name='adminpage'),
]