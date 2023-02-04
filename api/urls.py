from django.urls import path
from .views import ReviewDetailApiView

app_name = 'api'
urlpatterns = [
    path('review/<int:id>', ReviewDetailApiView.as_view(), name='review_detail'),
]
