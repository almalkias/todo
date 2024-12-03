from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import CustomUser, Category, Task

@receiver(post_save, sender=CustomUser)
def create_general_category(sender, instance, created, **kwargs):
    if created:  # Check if the user is being created
        # Check if the general category already exists
        if not Category.objects.filter(name='general', user=instance).exists():
            Category.objects.create(name='general', user=instance)


# @receiver(pre_save, sender=Task)
# def set_default_category(sender, instance, **kwargs):
#     if not instance.category:  # Check if no category is set
#         general_category = Category.objects.filter(name='general', user=instance.user).first()
#         if general_category:
#             instance.category = general_category
