from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from datetime import datetime
from django.utils import timezone



class Post(models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    reported_by = models.ManyToManyField(Profile,blank=True, related_name="reported_by")

    def to_dict(self):
        return{
            'pk': self.pk,
            'title': self.title,
            'content':self.content,
            'date_posted': self.date_posted.isoformat(),
            'author' : self.author.pk,
            'reported_by' : [r.user.pk for r in self.reported_by.all()]
        }

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(Profile,related_name='author',null=True,default='',on_delete=models.CASCADE)
    content = models.CharField(max_length=80)

    def to_dict(self):
        return{
            'pk': self.pk,
            'post': self.post.title,
            'comment':self.content,
            'author' : self.author.pk,
        }

    def __str__(self):
        return self.content     

