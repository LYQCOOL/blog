from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
class Diaries(models.Model):

    title=models.CharField(max_length=32,null=True)
    content=models.TextField()
    time=models.DateTimeField()
    author=models.ForeignKey(User,on_delete=True)
