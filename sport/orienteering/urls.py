from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api-token-auth', obtain_auth_token),
    path('auth/users/', 
         views.CustomParticipantCreateView.as_view({'post': 'create'}), 
         name='participant-create'
         ),
    path('auth/token/login/', views.CustomTokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.CustomTokenDestroyView.as_view(), name='logout'),
    path('auth/users/reset_password/', views.RequestPasswordResetView.as_view({'post': 'reset_password'}), name='reset-password'),
    path('auth/users/reset_password_confirm/', views.ConfirmPasswordResetView.as_view({'post': 'reset_password-confirm'}), name='reset-password-confirm'),
    path('auth/users/set_password/', views.SetPassword.as_view({'post': 'set_password'}), name='set-password')
]
