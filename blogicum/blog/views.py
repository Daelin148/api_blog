from blog.forms import CommentForm, PostForm
from blog.mixins import (
    CommentMixin, PostChangeMixin,
    CommentChangeMixin, ProfileRedirectMixin)
from blog.models import Category, Post, User
from blog.utils import get_valid_posts

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


class PostCreateView(ProfileRedirectMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


class PostUpdateView(PostChangeMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(PostChangeMixin, ProfileRedirectMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(CommentChangeMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentChangeMixin, DeleteView):

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


class ProfileEditView(ProfileRedirectMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self):
        return get_object_or_404(
            User,
            username=self.request.user.username
        )
