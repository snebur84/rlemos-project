from django.urls import path
from .views import (
    ListProjectsView,
    CreateProjectView,
    UpdateProjectView,
    DeleteProjectView,
    ListTasksView,
    CreateTaskView,
    UpdateTaskView,
    DeleteTaskView,
    ListProjectMembersView,
    CreateProjectMemberView,
    UpdateProjectMemberView,
    DeleteProjectMemberView
)

app_name = 'projects'
urlpatterns = [
    path('', ListProjectsView.as_view(), name='list_projects'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('update/<int:id>/', UpdateProjectView.as_view(), name='update_project'),
    path('delete/<int:id>/', DeleteProjectView.as_view(), name='delete_project'),
    
    path('tasks/', ListTasksView.as_view(), name='list_tasks'),
    path('tasks/create/', CreateTaskView.as_view(), name='create_task'),
    path('tasks/update/<int:id>/', UpdateTaskView.as_view(), name='update_task'),
    path('tasks/delete/<int:id>/', DeleteTaskView.as_view(), name='delete_task'),

    path('members/', ListProjectMembersView.as_view(), name='list_members'),
    path('members/create/', CreateProjectMemberView.as_view(), name='create_member'),
    path('members/update/<int:id>/', UpdateProjectMemberView.as_view(), name='update_member'),
    path('members/delete/<int:id>/', DeleteProjectMemberView.as_view(), name='delete_member'),
]