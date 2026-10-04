from django.db import models
from django.contrib.auth.models import AbstractUser

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