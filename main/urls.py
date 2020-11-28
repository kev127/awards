from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('accounts/register/', views.register, name='register'),
    path('profile/', views.profile,name = 'profile'),
    path('new_project/', views.new_project,name ='new_project'),
]