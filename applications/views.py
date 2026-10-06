from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from accounts.models import Resume
from .models import Application

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # 1. Ish beruvchilar ariza topshira olmaydi (Role tekshiruvi)
    user_role = str(getattr(request.user, 'role', '')).upper()
    if user_role == 'EMPLOYER' or getattr(request.user, 'is_employer', False):
        messages.error(request, "Ish beruvchilar vakansiyaga ariza topshira olmaydi!")
        return redirect('jobs:job_detail', pk=pk)

    # 2. Ish izlovchining Rezyumesi bor-yo'qligini tekshiramiz
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        messages.warning(request, "Ariza topshirishdan oldin rezyumengizni to'ldiring!")
        return redirect('accounts:edit_resume')

    # 3. Avval ariza topshirganligini tekshiramiz (Sizdagi 'seeker' maydoni bo'yicha)
    existing_app = Application.objects.filter(job=job, seeker=request.user).exists()
    if existing_app:
        messages.info(request, "Siz ushbu vakansiyaga allaqachon ariza topshirgansiz!")
        return redirect('jobs:job_detail', pk=pk)

    # 4. Arizani yaratamiz
    Application.objects.create(
        job=job,
        seeker=request.user,
        resume=resume
    )
    messages.success(request, "Arizangiz va rezyumengiz muvaffaqiyatli topshirildi! 🚀")
    return redirect('jobs:job_detail', pk=pk)
