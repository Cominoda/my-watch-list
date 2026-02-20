from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    #path('logout/', views.logout_user, name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('franceconnect/login/', views.fc_login, name="fc_login"),
    path('callback/', views.fc_callback, name="fc_callback"),
    path('franceconnect/logout/', views.fc_logout, name="fc_logout"),
]