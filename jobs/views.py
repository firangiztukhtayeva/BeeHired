from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Category, Company, Job
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .forms import JobForm, CompanyForm
from applications.models import Application

def home_view(request):
    return render(request, 'base.html')




def job_list(request):
    """Vakansiyalar ro'yxati va qidiruv/filtr oynasi"""
    jobs = Job.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Qidiruv (Sarlavha, kompaniya nomi yoki texnologiyalar bo'yicha)
    search_query = request.GET.get("q", "")
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query)
            | Q(company__name__icontains=search_query)
            | Q(technologies__icontains=search_query)
            | Q(location__icontains=search_query)
        )

    # Kategoriya bo'yicha filtr
    category_slug = request.GET.get("category", "")
    if category_slug:
        jobs = jobs.filter(category__slug=category_slug)

    # Ish turi bo'yicha filtr (Full-time, Remote va h.k.)
    job_type = request.GET.get("job_type", "")
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    context = {
        "jobs": jobs,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_slug,
        "selected_job_type": job_type,
    }
    return render(request, "jobs/job_list.html", context)


def job_detail(request, pk):
    """Vakansiya batafsil sahifasi"""
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    # O'xshash vakansiyalar
    related_jobs = Job.objects.filter(
        category=job.category, is_active=True
    ).exclude(pk=job.pk)[:3]

    # Nomzod ushbu vakansiyaga ariza topshirgan-topshirmaganini tekshiramiz
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, seeker=request.user).exists()

    context = {
        "job": job,
        "related_jobs": related_jobs,
        "has_applied": has_applied,  # Shablon uchun 'has_applied' o'zgaruvchisini uzatamiz
    }
    return render(request, "jobs/job_detail.html", context)  # yoki "jobs/job_detail.html"



@login_required
def job_create(request):
    """Yangi vakansiya yaratish"""
    print("--- DIAGNOSTIKA START ---")
    print("User Username:", request.user.username)
    print("User Role:", getattr(request.user, 'role', 'ROLE YOQ'))
    print("Has Company:", hasattr(request.user, 'company'))
    print("--- DIAGNOSTIKA END ---")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            if hasattr(request.user, "company"):
                job.company = request.user.company
            job.save()
            messages.success(request, "Vakansiya muvaffaqiyatli e'lon qilindi! 🚀")
            return redirect("jobs:job_detail", pk=job.pk)
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {"form": form})


@login_required
def company_edit(request):
    """Ish beruvchi uchun kompaniya profilini yaratish va tahrirlash"""
    if request.user.role != 'EMPLOYER':
        messages.error(request, "Bu sahifa faqat ish beruvchilar uchun!")
        return redirect('accounts:dashboard')

    # Foydalanuvchida kompaniya bor-yo'qligini tekshiramiz
    company = getattr(request.user, 'company', None)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.owner = request.user  # Kompaniya egasini biriktiramiz
            comp.save()
            messages.success(request, "Kompaniya ma'lumotlari muvaffaqiyatli saqlandi!")
            return redirect('accounts:dashboard')
    else:
        form = CompanyForm(instance=company)

    return render(request, 'jobs/company_form.html', {'form': form, 'company': company})

