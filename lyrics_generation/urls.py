from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'lyrics_generation'
urlpatterns = [
    # two paths: with or without given image
    path('', views.index, name='index'),
]
