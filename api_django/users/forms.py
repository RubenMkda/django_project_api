from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Projects, Technology

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

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
    technologies = forms.ModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Projects
        fields = ['url_image', 'url_code', 'url_repo', 'title', 'desp', 'technologies']

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Technology.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Esta tecnología ya existe.")
        return name.lower()