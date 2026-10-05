from django.contrib import admin
from .models import Category, Company, Job


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "created_at")
    search_fields = ("name", "location")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "category",
        "job_type",
        "is_active",
        "created_at",
    )
    list_filter = ("job_type", "is_active", "category")
    search_fields = ("title", "company__name", "location", "technologies")