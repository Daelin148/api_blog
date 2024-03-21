from django.urls import reverse
from blog.models import Comment, Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect


class PostChangeMixin(LoginRequiredMixin):
    """Миксин, добавляющий общие аттрибуты и метод проверки
    на авторство при изменении и удалении постов.
    """

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect(instance)
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    """Миксин с общими аттрибутами CBV для обработки комментариев."""

    model = Comment
    template_name = 'blog/comment.html'


class CommentChangeMixin(LoginRequiredMixin, CommentMixin):
    """Миксин, добавляющий общий метод
    для CBV удаления и изменения комментариев.
    """

    def get_object(self):
        obj = get_object_or_404(Comment.objects.select_related('author'),
                                pk=self.kwargs['comment_id'])
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj


class ProfileRedirectMixin(LoginRequiredMixin):
    """Миксин, добавляющий переадресацию на
    страницу профиля после отправки формы.
    """

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'author': self.request.user.username}
        )
