from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        USER = "USER", "User"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_staff_member(self):
        return self.role in [self.Role.ADMIN, self.Role.STAFF]
    
    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == self.Role.STAFF:
            self.is_staff = True
            self.is_superuser = False
        else:  # USER и любые будущие роли
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)