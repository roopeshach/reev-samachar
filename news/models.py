from django.db import models
from django.shortcuts import redirect
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True, null=True)
    url = models.CharField(max_length=254)
    image = models.CharField(max_length=254, default="", blank=True, null=True)
    date = models.CharField(max_length=254, default="", blank=True, null=True)
    author = models.CharField(max_length=254, default="", blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    
    
    



