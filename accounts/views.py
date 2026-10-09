from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Resume
from .forms import ResumeForm, ProfileUpdateForm
from jobs.models import Job
from applications.models import Application

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_validate() if hasattr(form, 'is_validate') else form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Muvaffaqiyatli ro'yxatdan o'tdingiz.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')  # yoki 'jobs:job_list'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Tizimga xush kelibsiz, {user.username}!")
            return redirect('accounts:dashboard')  # Tizimga kirgach dashboard sahifasiga yo'naltiriladi
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri kiritildi.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('jobs:job_list')  # Vakansiyalar ro'yxatiga/bosh sahifaga yo'naltiramiz


@login_required
def profile_dashboard(request):
    user = request.user
    context = {
        'user': user,
    }

    # Agar foydalanuvchi Ish beruvchi bo'lsa
    if user.role == 'EMPLOYER':
        # Ish beruvchining kompaniyasi bor-yo'qligini tekshiramiz (bo'lsa olamiz)
        company = getattr(user, 'company', None)
        context['company'] = company
        if company:
            context['jobs'] = company.jobs.all()
        else:
            context['jobs'] = []
    
    # Agar foydalanuvchi Ish izlovchi bo'lsa
    else:
        resume, created = Resume.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.get_full_name() or user.username,
                "title": "Dasturchi / Mutaxassis",
            }
        )
        context['resume'] = resume

    return render(request, "accounts/dashboard.html", context)

@login_required
def edit_resume(request):
    resume, created = Resume.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, request.FILES, instance=resume)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if resume_form.is_valid() and profile_form.is_valid():
            resume_form.save()
            profile_form.save()
            messages.success(request, "Profil va rezyume ma'lumotlari muvaffaqiyatli saqlandi!")
            return redirect('accounts:dashboard')
    else:
        resume_form = ResumeForm(instance=resume)
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_resume.html', {
        'form': resume_form,
        'profile_form': profile_form
    })
    



@login_required
def dashboard_view(request):
    user = request.user
    user_role = str(getattr(user, 'role', '')).upper()

    context = {}

    if user_role == 'EMPLOYER' or getattr(user, 'is_employer', False):
        # Ish beruvchining vakansiyalari
        my_jobs = Job.objects.filter(employer=user).order_by('-created_at')
        # Kelib tushgan tumandagi arizalar
        applications = Application.objects.filter(job__in=my_jobs).select_related('job', 'seeker', 'resume').order_by('-applied_at')
        
        context.update({
            'my_jobs': my_jobs,
            'applications': applications,
        })
    else:
        # Nomzodning rezyumesi
        resume = Resume.objects.filter(user=user).first()
        # Nomzod topshirgan arizalar
        my_applications = Application.objects.filter(seeker=user).select_related('job', 'job__employer').order_by('-applied_at')
        
        context.update({
            'resume': resume,
            'my_applications': my_applications,
        })

    return render(request, 'accounts/dashboard.html', context)