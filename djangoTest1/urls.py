from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('video/<int:id>', views.getVideo),
    path('video/<int:id>/likes',views.getLikes),
    path('video/<int:id>/comments',views.getComments),
    path('video/upload/',views.postVideo)
]
