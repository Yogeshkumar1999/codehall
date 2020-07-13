from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank=True, on_delete= models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 20, null = True)
    email = models.CharField(max_length = 200, null = True)
    profile_pic = models.ImageField(null = True, blank = True, default = 'logo.png')
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name

class Files(models.Model):
    file_name = models.FileField(null = True, blank = True)

    def __str__(self):
        self.file_name


class UserFiles(models.Model):
    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)
    #files = models.ManyToManyField(Files)
    name = models.CharField(null = True, max_length = 200)
    file_name = models.FileField(null = True, blank = True, upload_to = 'documents/')
    date_created = models.DateTimeField(auto_now_add = True, null = True)
    
    def __str__(self):
        return self.name

