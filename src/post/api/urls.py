from django.contrib import admin
from django.urls import path
from .views import BlogPostRUDView, BlogPostAPIView

app_name = "post.api"

urlpatterns = [
    path('', BlogPostAPIView.as_view(), name='post-create'),
    path('<int:pk>/', BlogPostRUDView.as_view(), name='post-rud'),
]
