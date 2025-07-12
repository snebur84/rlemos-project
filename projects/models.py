from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 

# Create your models here.
class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Progresso'),
        ('completed', 'Concluído')
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('projects:update_project', kwargs={'id': self.id})
    
    def get_delete_url(self):
        return reverse('projects:delete_project', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['start_date']

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Progresso'),
        ('completed', 'Concluído') 
    ]
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('projects:update_task', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('projects:delete_task', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['due_date']

class ProjectMember(models.Model):
    STATUS_CHOICES = [
        ('manager', 'Gerente'),
        ('supervisor', 'Supervisor'),
        ('colaborator', 'Colaborador')
    ]
    project = models.ForeignKey(Project, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='project_memberships', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=STATUS_CHOICES, default='colaborator')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
    
    def get_absolute_url(self):
        return reverse('projects:update_member', kwargs={'id': self.id})
    
    def get_delete_url(self):
        return reverse('projects:delete_member', kwargs={'id': self.id})