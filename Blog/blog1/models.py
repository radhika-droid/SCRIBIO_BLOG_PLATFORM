# blog1/models.py
# Add this to your existing models.py file

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default_profile.png')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'username': self.user.username})
    
    def follow(self, profile):
        """Follow another user's profile"""
        if profile != self:  # Prevent self-following
            self.following.add(profile)
    
    def unfollow(self, profile):
        """Unfollow another user's profile"""
        self.following.remove(profile)
    
    def is_following(self, profile):
        """Check if this profile follows another profile"""
        return self.following.filter(pk=profile.pk).exists()
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
