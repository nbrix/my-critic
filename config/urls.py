from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # Local apps
    path('', include('pages.urls')),
    path('movies/', include('movies.movies_urls')),
    path('critics/', include('movies.critics_urls')),
    path('ratings-quiz/', include('quiz.urls')),
]
