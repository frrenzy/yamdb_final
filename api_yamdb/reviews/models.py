from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import CreatedModel
from reviews.validators import year_validator
from users.models import User


class Genre(models.Model):
    name = models.CharField(
        'название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        'слаг жанра',
        unique=True,
        max_length=50,
        db_index=True,
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'название категории',
        max_length=256,
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        max_length=50,
        db_index=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название тайтла',
        max_length=256,
        db_index=True,
    )
    year = models.IntegerField(
        'год выпуска',
        validators=[year_validator],
    )
    description = models.TextField('описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre',
            )
        ]

    def __str__(self):
        return f'{self.title}: {self.genre}'


class Review(CreatedModel):
    text = models.TextField('текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'оценка',
        help_text='Поставьте оценку от 1 до 10',
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            ),
        ]

    def __str__(self):
        return self.text


class Comment(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('текст отзыва')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text
