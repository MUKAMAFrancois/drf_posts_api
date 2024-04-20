from django.db import models
from uuid import uuid4
from accounts.models import User

# Create your models here.


class UUIDField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', uuid4)
        super().__init__(*args, **kwargs)


class Post(models.Model):
    id = UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']