from django.db import models

class Category(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name