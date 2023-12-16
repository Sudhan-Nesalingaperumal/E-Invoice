from django.db import models


class Common(models.Model):
    # active = models.BooleanField(default=True)
    # created_date = models.DateTimeField(auto_now_add=True)
    # updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True