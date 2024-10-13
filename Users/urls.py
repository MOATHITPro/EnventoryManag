# from django.urls import path
# from . import views

# urlpatterns =[
#     path('signin', views.signin , name='signin'),
#     path('signup', views.signup , name='signup'),

# ]

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, manager_dashboard, operator_dashboard, login_redirect

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('operator_dashboard/', operator_dashboard, name='operator_dashboard'),
    path('redirect/', login_redirect, name='login_redirect'),
]
