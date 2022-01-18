from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Category')
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name='Author', null=True)

    def __str__(self):
        return self.title

class Ad(models.Model):
    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'
        ordering = ['-created_at']

    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField()
    image = models.ImageField(upload_to='ads/', verbose_name='Main image')
    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, verbose_name='User')
    created_at = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    surname = models.CharField(max_length=255, verbose_name='Surname')
    # posts = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='Posts')

    def __str__(self):
        return f'{self.name} {self.surname}'


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Comment(models.Model):
    comments = models.TextField(max_length=300, verbose_name='Comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    users = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='Users', null=True)

    def __str__(self):
        return self.comments