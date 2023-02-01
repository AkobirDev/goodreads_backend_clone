from django import forms

from books.models import BookReview

class ReviewForm(forms.ModelForm):
    stars = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = BookReview
        fields = ('stars', 'review_text')
        