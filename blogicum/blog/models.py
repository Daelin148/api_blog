from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

TITLE_LIMIT = 30
User = get_user_model()


class BlogModel(models.Model):
    """Абстрактная модель. Добавляет общие поля для всех моделей."""

    is_published = models.BooleanField(
        'Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(BlogModel):
    """Модель категорий публикаций."""

    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены'
            ' символы латиницы, цифры, дефис и подчёркивание.'),
        max_length=64,
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:TITLE_LIMIT]


class Location(BlogModel):
    """Модель локации публикаций."""

    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:TITLE_LIMIT]


class Post(BlogModel):
    """Модель публикаций."""

    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем —'
            ' можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:TITLE_LIMIT]

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.pk}
        )

    def comment_count(self):
        return Comment.objects.filter(post=self.pk).count()


class Comment(models.Model):
    """Модель комментариев к публикациям."""

    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    pub_date = models.DateTimeField(
        'Дата и время комментария',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('pub_date',)
        default_related_name = 'comments'

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.post.pk}
        )
