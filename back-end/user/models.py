from django.db import models

# Create your models here.

from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # fichier uploadé dans MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class Profile(models.Model):
    ROLE_CHOICES = [
        ('conducteur', 'Conducteur'),
        ('passager', 'Passager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to=user_directory_path, default='default_profile.png', blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.role}"

