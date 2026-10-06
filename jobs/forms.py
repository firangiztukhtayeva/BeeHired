from django import forms
from .models import Job, Company  # Company modelini qo'shdik


class CompanyForm(forms.ModelForm):
    """Ish beruvchi uchun kompaniya profili shakli"""
    class Meta:
        model = Company
        fields = ['name', 'logo', 'description', 'website', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Kompaniya nomi (masalan: Google)'}),
            'logo': forms.FileInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-secondary text-white border-0', 'rows': 4, 'placeholder': 'Kompaniya haqida qisqacha...'}),
            'website': forms.URLInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'https://company.com'}),
            'location': forms.TextInput(attrs={'class': 'form-control bg-secondary text-white border-0', 'placeholder': 'Masalan: Toshkent, O\'zbekiston'}),
        }


class JobForm(forms.ModelForm):
    """Vakansiya yaratish va tahrirlash shakli"""
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