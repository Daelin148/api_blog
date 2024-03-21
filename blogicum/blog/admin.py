from blog.models import Category, Comment, Location, Post

from django.contrib import admin

admin.site.empty_value_display = 'Не задано'


@admin.action(description='Опубликовать')
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'pub_date',
        'author',
        'is_published',
        'location'
    )
    list_editable = (
        'is_published',
        'category',
        'location',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    actions = (make_published,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
    )
    list_editable = (
        'slug',
        'is_published',
    )
    actions = (make_published,)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    actions = (make_published,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'created_at',
        'post',
        'author',
    )
    list_editable = (
        'text',
    )
