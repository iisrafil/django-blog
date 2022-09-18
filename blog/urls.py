from django.urls import path
from .views import (

    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView, home, pending_post, approve, CategoryListView, category_post
)
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', views.PostDetail, name='post-detail'),
    path('post-approve/<int:pk>/', approve, name='post-approve'),
    path('post/new/', PostCreateView, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/pending-post/', pending_post, name='pending-post'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('category/<int:pk>/', category_post, name='category-post'),
    path('about/', views.about, name='blog-about'),
]
