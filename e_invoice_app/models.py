from django.db import models
from generic_method.models import Common
# Create your models here.

class UserDetails(Common):


    gst = models.CharField('gst', max_length = 50, null = False,blank = False)
    username = models.CharField('username', max_length = 50, null = False,blank = False)
    password = models.CharField('password', max_length = 50, null = False,blank = False)
    date = models.CharField('date', max_length = 50, null = False,blank = False)

    class Meta:
        verbose_name_plural = "UserDetails"

    def __str__(self):
        return str(self.id)
