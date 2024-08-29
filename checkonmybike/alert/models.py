from django.db import models

from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.user.username})
