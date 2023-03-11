from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='time_slots/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
