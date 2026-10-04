from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,  Resume

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.Role.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Siz kimsiz?"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone_number')
        
        
from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name', 'title', 'phone', 'location', 
            'bio', 'skills', 'education', 'experience', 
            'github_link', 'linkedin_link'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Ferangiz To\'xtayeva'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Python / Django Backend Developer'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Buxoro, O\'zbekiston'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'O\'zingiz va maqsadingiz haqida qisqacha...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, C++, HTML, CSS, Git, PostgreSQL'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'O\'quv yurtingiz, bosqich va yo\'nalish...'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qayerda va qaysi lavozimda ishlagansiz...'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
        }        
        
        
        
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'phone_number']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
        }