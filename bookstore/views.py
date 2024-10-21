from django.shortcuts import render
from .models import Book
from .filters import BookFilter


def book_list(request):
    books = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=books)
    return render(request, 'book_list.html', {'filter': book_filter})
