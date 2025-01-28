from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import CustomUser, Category, Task, UserProfile
from django.contrib.auth import get_user_model

@receiver(post_save, sender=CustomUser)
def create_general_category(sender, instance, created, **kwargs):
    if created:  # Check if the user is being created
        # Check if the general category already exists
        if not Category.objects.filter(name='general', user=instance).exists():
            Category.objects.create(name='general', user=instance)


User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
