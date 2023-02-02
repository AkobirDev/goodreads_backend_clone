from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookReview

def landing_page(request):
    return render(request, 'landing.html')

def home_page(request):
    reviews = BookReview.objects.all().order_by('-created_at')
    
    page_size = request.GET.get('page_size', 10)
    page_num = request.GET.get('page', 1)
    
    pagination = Paginator(reviews, page_size)
    
    page_obj = pagination.get_page(page_num)

    context = {'page_obj': page_obj}

    return render(request, 'home.html', context)