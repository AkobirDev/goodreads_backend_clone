from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import BookReviewSerializer

from books.models import BookReview

# Create your views here.

class ReviewDetailApiView(APIView):
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

        return Response(data=serializer.data)