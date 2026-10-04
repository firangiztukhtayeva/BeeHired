from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYER = 'EMPLOYER', 'Ish beruvchi'
        JOB_SEEKER = 'JOB_SEEKER', 'Ish izlovchi'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.JOB_SEEKER,
        verbose_name="Foydalanuvchi roli"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Rasm")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Resume(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='resume',
        verbose_name="Foydalanuvchi"
    )
    full_name = models.CharField(max_length=255, verbose_name="To'liq ism-sharif")
    title = models.CharField(max_length=255, verbose_name="Mutaxassislik / Kasb yo'nalishi")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam", blank=True, null=True)
    location = models.CharField(max_length=100, verbose_name="Yashash manzili", blank=True, null=True)
    bio = models.TextField(verbose_name="O'zim haqimda", blank=True, null=True)
    skills = models.CharField(
        max_length=500, 
        verbose_name="Ko'nikmalar", 
        help_text="Masalan: Python, Django, HTML, CSS, Git", 
        blank=True, 
        null=True
    )
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Tajriba (yillar)")
    education = models.TextField(verbose_name="Ma'lumoti / Ta'lim", blank=True, null=True)
    experience = models.TextField(verbose_name="Ish tajribasi", blank=True, null=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="PDF Rezyume fayli")
    github_link = models.URLField(verbose_name="GitHub profili", blank=True, null=True)
    linkedin_link = models.URLField(verbose_name="LinkedIn profili", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.title}"