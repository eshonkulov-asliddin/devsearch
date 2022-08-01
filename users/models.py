from email import message
from email.policy import default
from platform import mac_ver
from pydoc import ModuleScanner
from pyexpat import model
import uuid
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True) 
    location = models.CharField(max_length=200, blank=True, null=True) 
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self) -> str:
        return str(self.username)

    class Meta():
        ordering = ['created']    

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = '../static/images/default.jpg'   
        return url     



class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, 
        null=True, blank=True)    
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self) -> str:
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['is_read', '-created']

        
    def __str__(self):
        return self.subject
        

    @property
    def unreadMessages(self):
        messages = self.filter(is_read=False).count()  

        self.unreadCount = messages  
        self.save()

