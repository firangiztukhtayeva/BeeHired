from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'category',
            'title',
            'description',
            'location',
            'job_type',
            'salary_min',
            'salary_max',
            'technologies',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select bg-secondary text-white border-0'}),
            'title': forms.TextInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Masalan: Senior Python Developer'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-secondary text-white border-0', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Toshkent yoki Remote'}),
            'job_type': forms.Select(attrs={'class': 'form-select bg-secondary text-white border-0'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Minimal maosh'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Maksimal maosh'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Python, Django, PostgreSQL'}),
        }