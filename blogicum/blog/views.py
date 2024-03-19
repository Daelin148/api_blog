from blog.forms import CommentForm, PostForm
from blog.models import Category, Comment, Post, User
from blog.utils import CommentMixin, get_valid_posts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'author': self.request.user}
        )


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        queryset = get_valid_posts()
        obj = get_object_or_404(queryset, pk=self.kwargs['post_id'])
        if self.request.user != obj.author:
            return get_object_or_404(
                get_valid_posts(is_guest=True,
                                queryset=queryset),
                pk=self.kwargs['post_id']
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        context['form'] = CommentForm()
        return context


class PostListView(ListView):
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return get_valid_posts(is_guest=True)


class CategoryListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        post_list = (
            get_valid_posts(is_guest=True).filter(
                category__slug=self.kwargs['category_slug'],
                category__is_published=True
            )
        )
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect(instance)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(instance=self.object)
        return context

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'author': self.request.user}
        )


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):

    def get_object(self):
        obj = get_object_or_404(Comment.objects.select_related('author'),
                                pk=self.kwargs['comment_id'])
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProfileListView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.username != self.kwargs['author']:
            return get_valid_posts(is_guest=True).filter(
                author__username=self.kwargs['author']
            )
        else:
            return get_valid_posts().filter(
                author__username=self.kwargs['author']
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['author']
        )
        return context


class ProfileEditView(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'author': self.request.user}
        )
