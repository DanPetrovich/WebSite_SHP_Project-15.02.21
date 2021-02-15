"""Example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from poll import views
from django.contrib.auth import views as auth_views

from poll.forms import UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('votings_shower', views.vote),
    path('concrete_voting', views.show_concrete_voting),
    path('voting_result', views.show_voting_result),
    path('choose_type', views.voting_type_choose),
    path('voting_ctor', views.voting_ctor),
    path('create_voting', views.create_voting),
    path("cabinet", views.cabinet),
    path('index', views.index, name='index_page'),
    path('edit', views.voting_editing),
    path('user_votings', views.user_votings),
    path('finish_editing', views.manage_voting),
    path('history', views.history),

    path('', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view()),
    path('registration/', views.signup),
    path('complaint/', views.complaint),
    path('complaint_ready/', views.complaint_done),
    path('complaint_list/', views.complaint_list),
    path('complaint_page/', views.complaint_page),
    path('complaint', views.complaint),
    path('complaint_ready/', views.complaint_done),

    path('settings', views.acc_settings),
    path('set', views.settings),
    path('editing', views.editing),
]
