from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from .forms import CustomUserCreationForm, ProjectsForm, TechnologyForm
from .models import Projects, Technology
from .serializers import ProjectsSerializer
from .permissions import IsAuthenticatedOrCreateOnly

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            
    else:
        form = AuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectsForm()
    user = request.user
    projects = Projects.objects.filter(user=user)
    context = {
        'title': 'Api projects',
        'projects': projects,
        'form': form
        }
    return render(request, 'pages/home.html', {'context': context})

@login_required
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    project.delete()
    return redirect('home')

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    if request.method == 'POST':
        form = ProjectsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectsForm(instance=project)
    return render(request, 'pages/update_project.html', {'form': form, 'project': project})

@login_required
def technologies(request):
    technologies = Technology.objects.all()
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            form.clean_name()
            form.save()
            return redirect('home')
    else:
        form = TechnologyForm()
    print(technologies)
    return render(request, 'pages/tech.html', {'form': form, 'technologies': technologies})

class ProjectsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get(self, request):
        projects = Projects.objects.all()
        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'pages/index.html')