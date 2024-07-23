from django.contrib.auth.models import User
from django.db import models

class Signature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signature_image = models.ImageField(upload_to='signatures/')

    def __str__(self):
        return f'{self.user.username}'
