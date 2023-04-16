from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.main, name='main'),
    path('video/', views.findVideo),
    path('video/watch/<int:id>', views.getVideo),
    path('video/<int:id>/scores', views.getLikes),
    path('video/<int:id>/comments', views.getComments),
    path('video/upload/', views.postVideo)
]