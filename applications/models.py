from django.db import models
from django.conf import settings
from jobs.models import Job, Resume

User = settings.AUTH_USER_MODEL

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Ko`rib chiqilmoqda'
        ACCEPTED = 'ACCEPTED', 'Qabul qilindi'
        REJECTED = 'REJECTED', 'Radd etildi'

    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name="Vakansiya"
    )
    seeker = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name="Ariza topshiruvchi"
    )
    resume = models.ForeignKey(
        Resume, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Biriktirilgan rezyume"
    )
    cover_letter = models.TextField(blank=True, verbose_name="Kuzatuv xati (Cover Letter)")
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Status"
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'seeker') # Bir foydalanuvchi bitta vakansiyaga faqat 1 marta topshirishi uchun constraint

    def __str__(self):
        return f"{self.seeker.username} -> {self.job.title} [{self.status}]"


class SavedJob(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='saved_jobs',
        verbose_name="Foydalanuvchi"
    )
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE,
        verbose_name="Saqlangan vakansiya"
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
