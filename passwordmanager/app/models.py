from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    favicon = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]