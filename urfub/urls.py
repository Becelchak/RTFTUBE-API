from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.main, name='main'),
    path('video/', views.findVideo, name='findVideo'),
    path('video/watch/<int:id>', views.getVideo, name='watchVideo'),
    path('video/liked/<int:id>', views.getLikes, name='likes'),
    path('video/disloked/<int:id>', views.getDislikes, name='dislikes'),
    path('video/upload/', views.postVideo, name='uploadVideo'),
    path('stream/<int:id>', views.getStreamVideo, name='stream')
]