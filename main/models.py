from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from tinymce.models import HTMLField

# Create your models here.
class Project(models.Model):
    title = models.TextField(max_length=30)
    image = models.ImageField(upload_to = 'main/', blank=True)
    link= models.URLField(max_length=200)
    description = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=True ,related_name='author')
    date_craeted= models.DateField(auto_now_add=True )
    


    def save_project(self):
        self.save()

    @classmethod
    def all_projects(cls) :
        projects = cls.objects.all()
        return projects


    @classmethod
    def search_by_title(cls,search_term):
        projects = cls.objects.filter(title__contains=search_term)
        return projects


     

    def __str__(self):
        return self.title

class Profile(models.Model):
    profile_pic = models.ImageField( upload_to='profile/', blank ='true')
    bio = models.TextField()
    user =models.OneToOneField(User, on_delete = models.CASCADE)
    date_craeted= models.DateField(auto_now_add=True )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.save
    
    def delete_user(self):
        self.delete()
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)