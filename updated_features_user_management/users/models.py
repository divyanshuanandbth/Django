from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    education = models.JSONField(default=list, blank=True, null=True)  # Store education as JSON
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def _str_(self):
        return f'{self.user.username} Profile'