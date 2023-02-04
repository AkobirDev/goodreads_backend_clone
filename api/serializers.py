from rest_framework import serializers
from books.models import Book, BookReview
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=200)
    # first_name = serializers.CharField(max_length=200)
    # last_name = serializers.CharField(max_length=200)
    # email = serializers.CharField(max_length=200)
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')

class BookSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=200)
    # description = serializers.CharField()
    # isbn = serializers.CharField(max_length=7)
    class Meta:
        model = Book
        fields = ('title', 'description', 'isbn')

class BookReviewSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    user = UserSerializer()
    book = BookSerializer()
    # review_text = serializers.CharField()
    # user = UserSerializer()
    # book = BookSerializer()
    class Meta:
        model = BookReview
        fields = ('stars', 'review_text', 'user', 'book')