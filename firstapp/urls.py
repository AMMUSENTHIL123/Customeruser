from django.urls import path

from . import views  # Assuming your views are defined in a views.py file within firstapp

urlpatterns = [
     path('', views.home, name='home'),  # Map the root URL to the home view
    path('login1', views.login1, name='login1'),  # Map the signup URL to the signup view
    path('student1', views.student1, name='student1'),  # Map the about URL to the about view
    path('teacher1', views.teacher1, name='teacher1'),
    path('studentsignup', views.studentsignup, name='studentsignup'),
    path('teachersignup', views.teachersignup, name='teachersignup'),
     path('ahome', views.ahome, name='ahome'),  # Map the root URL to the home view
     path('shome', views.shome, name='shome'),  # Map the root URL to the home view
     path('thome', views.thome, name='thome'),  # Map the root URL to the home view
     path('loginhome', views.loginhome, name='loginhome'),
     path('ad', views.ad, name='ad'),
      path('approve/<int:k>/', views.approve, name='approve'),
    path('disapprove/<int:k>/', views.disapprove, name='disapprove'),
    path('logout1', views.logout1, name='logout1'),
    path('resetpassword', views.resetpassword, name='resetpassword'),
    path('reset', views.reset, name='reset'),
]