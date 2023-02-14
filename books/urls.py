from django.urls import path
from .views import AddReviewView, \
BookDetailView, \
BookListView, \
EditReviewView, \
ConfirmDeleteReviewView, \
DeleteReviewView,  \
AuthorView 

app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:id>', BookDetailView.as_view(), name='detail'),
    path('<int:id>/review', AddReviewView.as_view(), name='reviews'),
    path('<int:book_id>/reviews/<int:review_id>/review/edit', EditReviewView.as_view(), name='review_edit'),
    path('<int:book_id>/reviews/<int:review_id>/review/delete/confirm', ConfirmDeleteReviewView.as_view(), name='review_delete_confirm'),
    path('<int:book_id>/reviews/<int:review_id>/review/delete', DeleteReviewView.as_view(), name='review_delete'),
    path('authors/<int:author_id>', AuthorView.as_view(), name='author_detail'),
]
