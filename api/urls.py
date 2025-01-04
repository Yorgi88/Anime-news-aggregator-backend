from django.urls import path
from .views import PostsView, GetLikedPostView, LikeUnlikePosts, Recommend

urlpatterns = [
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<int:post_id>/like/', LikeUnlikePosts.as_view(), name='like_unlike'),
    path('posts/liked/', GetLikedPostView.as_view(), name='liked_posts'),
    
]
