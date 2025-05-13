from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from .managers import PublishedManager
from django.utils.text import slugify

class Test(models.Model):
    testname = models.CharField(max_length=255)
    testlarsoni = models.IntegerField()
    testsavollari = models.TextField()
    testjavoblari = models.TextField()
    testmualiffi = models.ForeignKey(User, on_delete=models.CASCADE)

class AnswerTest(models.Model):
    tets_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer_author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_count = models.IntegerField()
    testishlanganvaqt = models.DateTimeField(auto_now_add=True)



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

    #save funksiyasini overrayt qlamiz
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsapp:detail_page', args=[self.slug])

class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return f"{self.name} {self.email}"

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Comment - {self.body} by {self.user}"

#####news1 = News.objects.create(news=5)
###news = reletad_name = comment
##user

class NewsLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'news'], name='unique_like')
        ]

    def __repr__(self):
        return f"{self.user} {self.news}"