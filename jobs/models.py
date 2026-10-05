from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    icon = models.CharField(
        max_length=50,
        default="bi-briefcase",
        help_text="Bootstrap icon klassi (masalan: bi-code-slash)"
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = "Kompaniya"
        verbose_name_plural = "Kompaniyalar"

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', "To'liq stavka (Full-time)"),
        ('part_time', "Yarim stavka (Part-time)"),
        ('remote', "Masofaviy (Remote)"),
        ('freelance', "Frilans (Freelance)"),
        ('internship', "Amaliyot (Internship)"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs',
        verbose_name="Kompaniya"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs',
        verbose_name="Kategoriya"
    )
    title = models.CharField(max_length=255, verbose_name="Vakansiya nomi")
    description = models.TextField(verbose_name="Tavsif va talablar")
    location = models.CharField(max_length=100, verbose_name="Joylashuv")
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='full_time',
        verbose_name="Ish turi"
    )
    salary_min = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Min maosh ($)"
    )
    salary_max = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Max maosh ($)"
    )
    technologies = models.CharField(
        max_length=255,
        help_text="Skill Match uchun kalit so'zlar (masalan: Python, Django, PostgreSQL)",
        verbose_name="Talab qilinadigan texnologiyalar"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Vakansiya"
        verbose_name_plural = "Vakansiyalar"

    def __str__(self):
        return f"{self.title} - {self.company.name}"