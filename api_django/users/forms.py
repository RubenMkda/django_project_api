from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Projects

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['url_image', 'url_code', 'url_repo', 'title', 'desp']