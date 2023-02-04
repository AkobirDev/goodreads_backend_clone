from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import BookReviewSerializer

from books.models import BookReview

# Create your views here.

class ReviewDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

        return Response(data=serializer.data)
    
class ReviewListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        bookreviews = BookReview.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(bookreviews, request)
        serializer = BookReviewSerializer(page_obj, many=True)

        return paginator.get_paginated_response(data=serializer.data)