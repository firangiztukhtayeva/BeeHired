from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Company(models.Model):
    owner = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='company',
        verbose_name="Egasining profili"
    )
    name = models.CharField(max_length=255, verbose_name="Kompaniya nomi")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Logotip")
    description = models.TextField(verbose_name="Kompaniya haqida")
    website = models.URLField(blank=True, null=True, verbose_name="Veb-sayt")
    location = models.CharField(max_length=100, verbose_name="Joylashuv/Shahar")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Resume(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='resume',
        verbose_name="Foydalanuvchi"
    )
    title = models.CharField(max_length=255, verbose_name="Kasb unvoni (Masalan: Python Backend Developer)")
    bio = models.TextField(blank=True, verbose_name="O'zi haqida qisqacha")
    skills = models.CharField(
        max_length=255, 
        help_text="Vergul bilan ajratib yozing (masalan: Python, Django, PostgreSQL)",
        verbose_name="Ko'nikmalar"
    )
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Tajriba (yillar)")
    file = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="PDF Rezyume fayli")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Job(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='jobs',
        verbose_name="Kompaniya"
    )
    title = models.CharField(max_length=255, verbose_name="Vakansiya nomi")
    description = models.TextField(verbose_name="Tavsif va talablar")
    location = models.CharField(max_length=100, verbose_name="Joylashuv")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Min maosh ($)")
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Max maosh ($)")
    technologies = models.CharField(
        max_length=255, 
        help_text="Skill Match uchun kalit so'zlar (masalan: Python, Django, PostgreSQL)",
        verbose_name="Talab qilinadigan texnologiyalar"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"
