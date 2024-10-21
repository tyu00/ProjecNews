import django_filters
from .models import Book, Publisher
from django.db.models import Q


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author = django_filters.CharFilter(lookup_expr='icontains', label='Автор')
    price = django_filters.RangeFilter(label='Цена от до')
    publisher = django_filters.ModelChoiceFilter(queryset=Publisher.objects.all(), label='Издатель')
    term = django_filters.CharFilter(method='filter_term', label='')

    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'publisher', 'term']

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(title__icontains=term) | Q(author__icontains=term)

        return queryset.filter(criteria).distinct()
