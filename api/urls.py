from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookReviewViewset 

app_name = 'api'
router = DefaultRouter()
router.register('reviews',BookReviewViewset, basename='review')
urlpatterns = router.urls