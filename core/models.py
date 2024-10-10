from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='Автор')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    photo = models.ImageField(upload_to='photos/%Y/%m/d/', verbose_name='Фото', blank=True, null=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def is_published(self):
        return self.status == 'published'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def article_count(self):
        return self.articles.count()


class ArticleCategory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'category')
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статей'

    def __str__(self):
        return f'{self.article} - {self.category}'


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author} на {self.article}'

    def is_recent(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).days < 1

    def get_author_username(self):
        return self.author.username


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def get_excerpt(self, length=100):
        return self.content[:length] + ('...' if len(self.content) > length else '')


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'tag')
        verbose_name = 'Тег статьи'
        verbose_name_plural = 'Теги статей'

    def __str__(self):
        return f'{self.article} - {self.tag}'
