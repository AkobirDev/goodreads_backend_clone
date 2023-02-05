from django.urls import path
from .views import ReviewDetailApiView, ReviewListApiView

app_name = 'api'
urlpatterns = [
    path('reviews/', ReviewListApiView.as_view(), name='review_list'),
    path('reviews/<int:id>', ReviewDetailApiView.as_view(), name='review_detail'),
]
