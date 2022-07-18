from django.urls import path
from .views import projects, project, CreateProject, updateProject, deleteProject

urlpatterns = [
    path('', projects, name='projects'),
    path('project/<str:pk>/', project, name='project'),
    
    path('create-project', CreateProject, name='create-project'),
    path('update-project/<str:pk>/', updateProject, name='update-project'),
    path('delete-project/<str:pk>/', deleteProject, name='delete-project'),

]