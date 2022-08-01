from distutils.command.upload import upload
from django.db import models
from django.db import models
import uuid
from users.models import Profile

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, blank=True, null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta():
        ordering = ['-vote_ratio', '-vote_total', 'title']

    def __str__(self) -> str:
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = 'https://devsearch-img-bucket.s3.us-west-2.amazonaws.com/default.jpg'   
        return url                     

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio    

        self.save()



class Review(models.Model):
    VOTE_TYPE =     (
        ('up', 'Up Vote'),
        ('down', 'down Vote'),
        
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)   

    
    def __str__(self) -> str:
        return self.name     