from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import home_page, landing_page

urlpatterns = [
    path('users/', include('users.urls'), name='users'),
    path('books/', include('books.urls'), name='books'),
    path('api/', include('api.urls'), name='api'),
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('home', home_page, name='home_page'),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

