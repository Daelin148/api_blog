from blog.models import Comment, Post
from django.utils import timezone


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'


def get_valid_posts(is_guest=False, queryset=None):
    """Функция, получающая QuerySet постов
    в зависимости от страницы отображения.

    Автор поста может получить объект, даже если:
    1. Пост снят с публикации;
    2. Дата публикации установлена в будущем;
    3. Категория поста снята с публикации.
    """
    if queryset is None:
        posts = Post.objects.select_related(
            'author', 'category', 'location'
        )
    else:
        posts = queryset
    if is_guest:
        current_date = timezone.now()
        posts = posts.filter(
            is_published=True,
            pub_date__lte=current_date,
            category__is_published=True,
        )
    return posts
