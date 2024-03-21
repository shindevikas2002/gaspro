from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
  #  path('', views.index, name='index'),
     path('submitreq/', views.submitreq, name='submitreq'),
         path('track/', views.track, name='track'),
                  path('login/', views.login, name='login'),
                  path('logincust1/', views.logincust1, name='logincust1'),

                  path('update_status/', views.update_status, name='update_status'),
                  path('account/', views.account, name='account'),



                  path('register_customer1/', views.register_customer1, name='register_customer1'),

   
]