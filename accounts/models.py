from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg") #guardá un default.png en /media/avatars/

    def __str__(self):
        return f"Perfil de {self.user.username}"


#el perfil se crea automatico al registrar un usuario
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()