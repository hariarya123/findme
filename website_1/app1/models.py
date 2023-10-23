  
from django.db import models
from django.core.validators import validate_image_file_extension
import os

def upload_to(instance, filename):
    # Get the filename from the URL
    filename = os.path.basename(filename)
    return f'images/{filename}'

class finepage(models.Model):
    img = models.ImageField(upload_to='images/', null=True, blank=True, validators=[validate_image_file_extension])
    price = models.FloatField()
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    address=models.CharField(max_length=400)
    emg=models.CharField(max_length=5)
    url_field = models.URLField(max_length=2000)
    ur_rl=models.URLField(max_length=8000)


    def __str__(self):
        return self.name
    
class register(models.Model):
    username = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    number=models.FloatField()
    password=models.CharField(max_length=30)