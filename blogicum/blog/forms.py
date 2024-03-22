from blog.models import Comment, Post

from django import forms
from django.utils import timezone


class PostForm(forms.ModelForm):
    """Форма публикации."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        exclude = ('author', )
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local',
                       'class': 'form-control'}
            ),
        }


class CommentForm(forms.ModelForm):
    """Форма комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
