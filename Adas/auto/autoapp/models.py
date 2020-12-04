from django.db import models

# Create your models here.
import os

from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath(__file__)))

class auto_users(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    uname = models.CharField(max_length=20)
    pwd  = models.CharField(max_length=20)


class upload(models.Model):
    filepaths = models.FileField(max_length=200,upload_to=os.path.join(BASE_DIR,'filepaths'))
    filename = models.CharField(max_length=50)
    user_id = models.ForeignKey(auto_users, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=timezone.now)


class cleanData(models.Model):
    filepaths_clean = models.FileField(max_length=200, upload_to=os.path.join(BASE_DIR, 'filepaths_clean'))
    filename_clean = models.CharField(max_length=50)
    clean_date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(auto_users, on_delete=models.CASCADE)



