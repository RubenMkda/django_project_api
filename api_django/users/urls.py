from django.urls import path
from .views import register, home, login_view, index, delete_project, update_project, technologies,ProjectsView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('projects/<int:project_id>/update/', update_project, name='update_project'),
    path('api/projects/', ProjectsView.as_view(), name='api-projects'),
    path('technologies', technologies, name='technologies')
]