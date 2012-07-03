from django.db import models
from django.contrib.auth.models import User

class Tweets(models.Model):
    image = models.CharField(max_length=300)
    handler = models.CharField(max_length=50, null=False)
    tweet_id = models.CharField(max_length=25,null=False)
    created = models.CharField(max_length=30, null=False)
    text = models.CharField(max_length=140, null=False, unique=True)
    source = models.CharField(max_length=300, null=True)

    def __unicode__(self):
        return self.handler    

class Follow(models.Model):
    handler = models.CharField(max_length=30, null=False, unique=True)
    
    def __unicode__(self):
        return self.handler

class Usr(models.Model):
    user = models.ForeignKey(User)
    following = models.CharField(max_length=30, null=False)

    def __unicode__(self):
        return self.user.username
