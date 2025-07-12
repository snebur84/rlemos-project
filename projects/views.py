from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import ProjectSerializer
from .forms import ProjectForm, TaskForm, ProjectMemberForm
from .models import Project, Task, ProjectMember

# Create your views here.
class ListProjectsView(ListView):
    model = Project
    template_name = 'projects/list_projects.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.all()
    
class CreateProjectView(CreateView):
    model = Project
    template_name = 'projects/edit_project.html'
    form_class = ProjectForm

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:list_projects')
    
class UpdateProjectView(UpdateView):
    model = Project
    template_name = 'projects/edit_project.html'
    form_class = ProjectForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Project, id=id)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:list_projects')
    
class DeleteProjectView(DeleteView):
    model = Project

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Project, id=id)
    
    def get_success_url(self):
        return reverse('projects:list_projects')
    
class ListTasksView(ListView):
    model = Task
    template_name = 'projects/list_project_tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.all()

class CreateTaskView(CreateView):
    model = Task
    template_name = 'projects/edit_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:list_tasks')
    
class UpdateTaskView(UpdateView):
    model = Task
    template_name = 'projects/edit_task.html'
    form_class = TaskForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Task, id=id)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:list_tasks')
    
class DeleteTaskView(DeleteView):
    model = Task

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Task, id=id)
    
    def get_success_url(self):
        return reverse('projects:list_tasks')
    
class ListProjectMembersView(ListView):
    model = ProjectMember
    template_name = 'projects/list_project_members.html'
    context_object_name = 'members'
    paginate_by = 10

    def get_queryset(self):
        return ProjectMember.objects.all()
    
class CreateProjectMemberView(CreateView):
    model = ProjectMember
    template_name = 'projects/edit_project_member.html'
    form_class = ProjectMemberForm

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:list_members')
    
class UpdateProjectMemberView(UpdateView):
    model = ProjectMember
    template_name = 'projects/edit_project_member.html'
    form_class = ProjectMemberForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(ProjectMember, id=id)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:list_members')
    
class DeleteProjectMemberView(DeleteView):
    model = ProjectMember

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(ProjectMember, id=id)
    
    def get_success_url(self):
        return reverse('projects:list_members')

class ProjectViewSet(viewsets.ModelViewSet):
    """
    **GERENCIAMENTO DE PROJETOS**

    Este endpoint permite o gerenciamento de projetos, incluindo a criação, leitura, atualização e exclusão de projetos.
    Os projetos compõem a base central do sistema, permitindo a organização e acompanhamento de tarefas e membros associados.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
  
class CustomAuthToken(ObtainAuthToken):
    """
    **AUTENTICAÇÃO DE USUÁRIO**
    Este endpoint permite a autenticação de usuários via token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })
    