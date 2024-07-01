from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(User):
    elo = models.FloatField(default=1000)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f'{self.username} - Account'
    
    def get_rounded_elo(self):
        """ Returns Elo rounded down, use for display """
        return int(self.elo)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_name = models.TextField(max_length=25)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    def get_profile_info(self):
        """ Returns a dict of profile info """
        return {
            'user' : self.user.id,
            'elo' : self.user.elo,
            'name' : self.profile_name,
            'bio' : self.bio
        }

    def __str__(self):
        return f'{self.user.username} - Profile'
