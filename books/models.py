from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.



class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_img = models.ImageField(default='cover.png')
    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    bio = models.TextField(blank=True, null=True)
    author_photo = models.ImageField(default='default-user-pic.jpg')

    def fullName(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.book.title} {self.author.first_name} {self.author.last_name}"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.stars} for {self.book.title} by {self.user.username}"
