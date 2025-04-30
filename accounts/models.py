from django.db import models
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    Phone_number = models.CharField(max_length=15, blank=False, null=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.user.username