from django.db import models

# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()


class Feature(models.Model):
    icon = models.ImageField(upload_to='Feature/icon/')
    title = models.CharField(max_length=255)
    text = models.TextField()
    