from django.contrib import admin
from .models import Article, Category, Comment, Tag, ArticleTag, ArticleCategory


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'status', 'photo_display')
    list_filter = ('status', 'published_date', 'author')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)

    def photo_display(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" style="width: 50px; height: auto;" />'
        return "Нет фото"

    photo_display.allow_tags = True
    photo_display.short_description = 'Фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('article', 'category')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at', 'article')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag')
