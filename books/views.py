from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View, ListView, DetailView

from books.forms import ReviewForm
from .models import Book, BookReview

# Create your views here.

# class BookListView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2


class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains = search_query)
        page_size = request.GET.get('page_size', 2)
        pagination = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = pagination.get_page(page_num)

        context = {'page_obj': page_obj, 'search_query': search_query}
        return render(request, 'books/list.html', context)


# class BookDetailView(DetailView):
#     template_name = 'books/book_detail.html'
#     pk_url_kwarg = 'id'
#     model = Book


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = ReviewForm()
        context = {'book': book, 'review_form': review_form}
        return render(request, 'books/book_detail.html', context)

class AddReviewView(LoginRequiredMixin,View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = ReviewForm(data=request.POST)
        user = request.user
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=user,
                stars=review_form.cleaned_data['stars'],
                review_text=review_form.cleaned_data['review_text']
            )
        else:
            context = {'book': book, 'review_form': review_form}
            return render(request, 'books/book_detail.html', context)
        return redirect(reverse('books:detail', kwargs={'id':book.id}))


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_edit_form = ReviewForm(instance=review)

        context = {'book': book, 'review_edit_form': review_edit_form, 'review': review}
        return render(request, 'books/review_edit.html', context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_edit_form = ReviewForm(instance=review, data=request.POST)
        
        if review_edit_form.is_valid:
            review_edit_form.save()
        else:
            context = {'book': book, 'review_edit_form': review_edit_form, 'review': review}
            return render(request, 'books/review_edit.html', context)
        return redirect(reverse('books:detail', kwargs={'id': book.id}))


class ConfirmDeleteReviewView(View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        context = {'book': book, 'review': review, }
        return render(request, 'books/review_delete_confirm.html', context)    


class DeleteReviewView(View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review.delete()
        messages.success(request, 'You have successfully deleted the review!')
        return redirect(reverse('books:detail', kwargs={'id': book.id}))