from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

# Create your models here.


class Book(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=150)
    about = models.TextField()
    summary = models.TextField()
    cover = models.ImageField(
        upload_to="books/covers/",
    )
    pages = models.PositiveSmallIntegerField()

    genres = models.ManyToManyField("Genre", related_name="books")
    star = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    publisher = models.CharField(max_length=150)
    published_date = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title[:20]


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
