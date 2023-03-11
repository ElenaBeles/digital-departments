from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField
    counts_likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='time_slots/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
