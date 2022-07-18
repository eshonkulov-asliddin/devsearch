# TRIGGERS
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User

from devsearch.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from .models import Profile, Skill

from django.core.mail import send_mail
from django.conf import settings






# @receiver(post_save, sender=Profile)
def CreateProfile(sender, created, instance, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        send_mail(
            subject= 'Welcome to DevSearch!',
            message='We are glad that you are here',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[profile.email],
            fail_silently=False
        )

def UpdateProfile(sender, created, instance, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# def addSkill(sender, instance, created, **kwargs):
#     profile =  instance

#     if created:
#        profile.     

# @receiver(post_save, sender=Profile)
def DeleteProfile(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()                
    except:
        pass

post_save.connect(CreateProfile, sender=User)    
post_save.connect(UpdateProfile, sender=Profile)    
# post_save.connect(userUpdate, sender=Skill)    
post_delete.connect(DeleteProfile, sender=Profile)