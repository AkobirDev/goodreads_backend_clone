from django.urls import path
from .views import AddReviewView, BookDetailView, BookListView

app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:id>', BookDetailView.as_view(), name='detail'),
    path('<int:id>/review', AddReviewView.as_view(), name='reviews'),
]
