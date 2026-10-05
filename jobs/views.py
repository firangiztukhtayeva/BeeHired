from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Category, Company, Job
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import JobForm

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
    related_jobs = Job.objects.filter(
        category=job.category, is_active=True
    ).exclude(pk=job.pk)[:3]

    context = {
        "job": job,
        "related_jobs": related_jobs,
    }
    return render(request, "jobs/job_detail.html", context)



@login_required
def job_create(request):
    """Yangi vakansiya yaratish"""
    # Foydalanuvchiga bog'langan kompaniyalik tekshiruvi
    if not hasattr(request.user, "company"):
        return redirect("jobs:job_list")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            return redirect("jobs:job_detail", pk=job.pk)
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {"form": form})