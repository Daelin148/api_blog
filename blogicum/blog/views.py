from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

POSTS_ON_MAIN = 5


def get_valid_posts():
    current_date = timezone.now()
    posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=current_date,
        category__is_published=True,
    )
    return posts


def index(request):
    posts = get_valid_posts()[:POSTS_ON_MAIN]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        get_valid_posts(),
        pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_list_or_404(
        get_valid_posts(),
        category__slug=category.slug
    )
    return render(request,
                  'blog/category.html',
                  {'post_list': post_list,
                   'category': category})
