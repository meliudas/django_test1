from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name='Автор', null=True)

    def __str__(self):
        return self.title

class Author (models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')

    def __str__(self):
        return f'{self.name} {self.last_name}'

class CastomUser(AbstractUser):
    login = models.CharField(max_length=32, verbose_name='Логин')
    name = models.CharField(max_length=255, verbose_name='Имя', blank=True, null=True)

    def __str__(self):
        return self.login

class Comments(models.Model):
    text = models.TextField(max_length=300, verbose_name='Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CastomUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.text if self.text else str(self.user)
