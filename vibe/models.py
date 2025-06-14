from django.db import models

# Create your models here.


class Request(models.Model):
    message=models.TextField(max_length=1000)


    
    def __str__(self) -> str:
        return self.message
    
