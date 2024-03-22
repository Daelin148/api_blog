from django.db import models


class CreatedAt(models.Model):
    """Абстрактная модель, добавляющая поле даты добавления."""

    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class IsPublishedCreatedAt(CreatedAt):
    """Абстрактная модель. Добавляет общие поля для всех моделей."""

    is_published = models.BooleanField(
        'Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )

    class Meta:
        abstract = True
