from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ArticleQuerySet(models.QuerySet):
    def annotate_time(self):
        return self.annotate(F("created_at"))


class Article(models.Model):
    objects = ArticleQuerySet.as_manager()

    title = models.CharField(max_length=50)
    created_at = models.DateTimeField
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
