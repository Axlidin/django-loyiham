from django.db import models
from django.utils import timezone
from .managers import PublishedManager


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class News(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', "Draft"
        Published = "PB", "Published"
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, default=Status.Draft, choices=Status.choices)

    objects = models.Manager()  # defalt maneger
    published = PublishedManager()# custom managers

    class Meta:
        ordering = ['-published_time']

    def __str__(self):
        return self.title
