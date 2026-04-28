from .models import UserProfile, User
from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=UserProfile)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.userprofile.save()
        except:
            UserProfile.objects.create(user=instance)
            
