from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('description',)
    search_fields = (
        'name',
        'description',
        'genre',
        'category',
    )
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'title',
        'author',
        'score',
    )
    search_fields = (
        'title',
        'author',
    )
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'review',
        'author',
    )
    search_fields = (
        'review',
        'author',
    )
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
