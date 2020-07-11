from django.db import models
from PIL import Image
from django.contrib.auth.models import User
# Signals
from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    about = models.CharField(max_length=140,null=True)
    follows = models.ManyToManyField('self',symmetrical=False,related_name='following')
  
# Best-practice for serializers(include within model)

    def to_dict(self):
        return {
            'pk': self.pk,
            'user': self.user.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'about' : self.about,
            'follows': [f.to_dict() for f in self.follows.all()],
        }

    def __str__(self):
        return f"{self.first_name}'s Profile"

# Modify the save method

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
       
        if img.height > 400 or img.width > 400:
            output_size = (300,350)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Signals for creating & updating Profile

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

@receiver(post_save,sender=User)
def update_profile(sender,instance,**kwargs):
    instance.profile.save()            

