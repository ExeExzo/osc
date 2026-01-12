from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Camp(models.Model):
    name = models.CharField("Название лагеря", max_length=150)
    location = models.CharField("Местоположение", max_length=255)
    description = models.TextField("Описание", blank=True)

    start_date = models.DateField("Начало смены", null=True, blank=True)
    end_date = models.DateField("Конец смены", null=True, blank=True)

    capacity = models.PositiveIntegerField("Максимум детей", default=0)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} — {self.location}"

    @property
    def approved_count(self):
        return self.registrations.filter(status="approved").count()

    @property
    def free_places(self):
        return max(self.capacity - self.approved_count, 0)


class CamperRegister(models.Model):
    full_name = models.CharField("ФИО ребёнка", max_length=255)
    iin = models.CharField("ИИН", max_length=12, unique=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campers",
        null=True,
        blank=True
    )
    uploaded_id = models.FileField("PDF удостоверения", upload_to="campers_ids/")
    created_at = models.DateTimeField(auto_now_add=True)

    camp = models.ForeignKey(Camp,on_delete=models.SET_NULL, null=True, blank=True, related_name="registrations"
    )

    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("approved", "Одобрен"),
        ("rejected", "Отклонён"),
    ]
    status = models.CharField(
        "Статус заявки",
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return f"{self.full_name} — {self.camp.name if self.camp else 'Без лагеря'}"
    

class CampParticipant(models.Model):
    camper = models.ForeignKey(
        CamperRegister,
        on_delete=models.CASCADE,
        related_name="participations"
    )
    camp = models.ForeignKey(
        Camp,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    approved_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField("Дата начала смены")
    end_date = models.DateField("Дата окончания смены")

    class Meta:
        unique_together = ("camper", "camp")
        verbose_name = "Участник лагеря"
        verbose_name_plural = "Участники лагеря"

    def __str__(self):
        return f"{self.camper.full_name} — {self.camp.name}"