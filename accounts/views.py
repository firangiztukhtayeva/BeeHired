from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ResumeForm, ProfileUpdateForm
from .models import Resume
from jobs.models import Job
from applications.models import Application


def register_view(request):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Muvaffaqiyatli ro'yxatdan o'tdingiz. 🚀")
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Tizimga kirish"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Tizimga xush kelibsiz, {user.username}!")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri kiritildi.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Tizimdan chiqish"""
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect('jobs:job_list')


@login_required
def dashboard_view(request):
    """Shaxsiy kabinet (Ish beruvchi va Ish izlovchi uchun)"""
    user = request.user
    user_role = str(getattr(user, 'role', '')).upper()

    context = {}

    if user_role == 'EMPLOYER' or getattr(user, 'is_employer', False):
        # Ish beruvchining kompaniyasi va e'lon qilgan vakansiyalari
        company = getattr(user, 'company', None)
        my_jobs = Job.objects.filter(company=company).order_by('-created_at') if company else Job.objects.filter(employer=user).order_by('-created_at')
        
        # Kelib tushgan arizalar
        applications = Application.objects.filter(job__in=my_jobs).select_related('job', 'seeker', 'resume').order_by('-applied_at')

        context.update({
            'role': 'EMPLOYER',
            'company': company,
            'my_jobs': my_jobs,
            'applications': applications,
        })
    else:
        # Ish izlovchining rezyumesi (bo'lmasa avtomatik yaratamiz)
        resume, created = Resume.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.get_full_name() or user.username,
                "title": "Dasturchi / Mutaxassis",
            }
        )
        # Nomzod topshirgan arizalar
        my_applications = Application.objects.filter(seeker=user).select_related('job', 'job__company').order_by('-applied_at')

        context.update({
            'role': 'SEEKER',
            'resume': resume,
            'my_applications': my_applications,
        })

    return render(request, 'accounts/dashboard.html', context)


@login_required
def edit_resume(request):
    """Rezyume va Profil ma'lumotlarini tahrirlash"""
    resume, created = Resume.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.get_full_name() or request.user.username,
            "title": "Dasturchi / Mutaxassis",
        }
    )

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, request.FILES, instance=resume)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if resume_form.is_valid() and profile_form.is_valid():
            resume_form.save()
            profile_form.save()
            messages.success(request, "Profil va rezyume ma'lumotlari muvaffaqiyatli saqlandi! 💾")
            return redirect('accounts:dashboard')
    else:
        resume_form = ResumeForm(instance=resume)
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_resume.html', {
        'form': resume_form,
        'profile_form': profile_form
    })