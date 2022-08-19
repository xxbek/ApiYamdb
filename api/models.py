from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

from .utils import date_not_in_future


class UserRoles(models.TextChoices):
    """class for user roles"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class NewUser(AbstractUser):
    """Class for user representation"""
    email = models.EmailField(unique=True, db_index=True, verbose_name='Электронная почта')
    confirmation_code = models.CharField(max_length=100, blank=True, unique=True, null=True, editable=True,
                                         verbose_name='Код подтверждения')

    bio = models.TextField(blank=True, verbose_name='Об авторе')
    role = models.CharField(max_length=50, choices=UserRoles.choices, default=UserRoles.USER,
                            verbose_name='Представление')

    def __str__(self):
        return self.email


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(validators=[date_not_in_future])
    description = models.TextField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='titles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name='categories')


class Review(models.Model):
    text = models.TextField(max_length=6000, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    scope = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    pub_date = models.DateField(auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews',
                              verbose_name='Произведение', null=True)


class Comments(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments', null=True)

