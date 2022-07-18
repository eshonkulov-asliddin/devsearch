from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
    path('account/', views.userAccount, name='user-account'),
    path('edit-account/', views.editAccount, name='edit-account'),  

    path('add-skill/', views.addSkill, name='add-skill'),    
    path('edit-skill/<str:pk>/', views.editSkill, name='edit-skill'),    
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),    


    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('inbox/', views.inboxMessages, name='inbox-messages'),
    path('message/<str:pk>/', views.viewMessage, name='single-message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message'),
]    