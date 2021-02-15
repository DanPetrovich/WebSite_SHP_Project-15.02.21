from django.db import models


class Calculation(models.Model):
    first = models.IntegerField()
    second = models.IntegerField()
    result = models.IntegerField()
