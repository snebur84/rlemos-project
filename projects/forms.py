from django import forms
from .models import Project, Task, ProjectMember
from django.contrib.auth.models import User 

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, 
        label="Nome do Projeto",
        error_messages={
            'required': 'Este campo é obrigatório.',
            'max_length': 'O nome do projeto não pode exceder 100 caracteres.' 
        }
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=False,
        label="Descrição do Projeto"
    )
    start_date = forms.DateField(
        widget=DateInput(),
        label="Data de Início",
        error_messages={
            'required': 'A data de início é obrigatória.'
        }
    )
    end_date = forms.DateField(
        widget=DateInput(),
        required=False,
        label="Data de Término"
    )
    status = forms.ChoiceField(
        choices=Project.STATUS_CHOICES, 
        label="Status do Projeto"
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date', 'end_date']



class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        label="Título da Tarefa",
        error_messages={
            'required': 'O título da tarefa é obrigatório.',
            'max_length': 'O título não pode exceder 200 caracteres.'
        }
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Descrição da Tarefa"
    )
    due_date = forms.DateField(
        widget=DateInput(),
        required=False,
        label="Data de Vencimento"
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all().order_by('name'), 
        label="Projeto",
        error_messages={'required': 'Selecione um projeto para a tarefa.'}
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(), 
        required=False,
        label="Atribuído a",
        error_messages={'invalid_choice': 'O usuário selecionado não é válido para este projeto.'}
    )
    status = forms.ChoiceField(
        choices=Task.STATUS_CHOICES, 
        label="Status",
        error_messages={'required': 'O status da tarefa é obrigatório.'}
    )

    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assigned_to', 'due_date', 'status']

    
    def __init__(self, *args, **kwargs):
        project_instance = kwargs.pop('project_instance', None)
        super().__init__(*args, **kwargs)

        if project_instance:
            member_users_ids = ProjectMember.objects.filter(project=project_instance).values_list('user__id', flat=True)
            self.fields['assigned_to'].queryset = User.objects.filter(id__in=member_users_ids).order_by('username')
        elif self.instance.pk and self.instance.project:
            member_users_ids = ProjectMember.objects.filter(project=self.instance.project).values_list('user__id', flat=True)
            self.fields['assigned_to'].queryset = User.objects.filter(id__in=member_users_ids).order_by('username')
        else:
            pass 

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-control'
            
            if field_name == 'project':
                field.widget.attrs['class'] += ' project-select'

    def clean_assigned_to(self):
        assigned_to_user = self.cleaned_data.get('assigned_to')
        project = self.cleaned_data.get('project')

        if assigned_to_user and project:
            if not ProjectMember.objects.filter(project=project, user=assigned_to_user).exists():
                raise forms.ValidationError("O usuário atribuído deve ser um membro do projeto selecionado.")
        return assigned_to_user

class ProjectMemberForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all().order_by('name'),
        label="Projeto",
        error_messages={'required': 'Selecione um projeto.'}
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        label="Usuário",
        error_messages={'required': 'Selecione um usuário.'}
    )
    role = forms.ChoiceField(
        choices=ProjectMember.STATUS_CHOICES, 
        label="Papel",
        error_messages={'required': 'Defina um papel para o membro.'}
    )
    phone = forms.CharField(max_length=15, required=False, label="Telefone")
    mail = forms.EmailField(required=False, label="Email")


    class Meta:
        model = ProjectMember
        fields = ['project', 'user', 'role', 'phone', 'mail'] 

