from django.shortcuts import render
from .serializers import UserSerializer, PostSerializer
from .models import Posts, LikedPost
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

class PostsView(generics.ListAPIView):
    """view to list all post, only
    authenticated users can access this
    ListAPIView only supports GET reqs, so user can only view posts , not make them"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """returns all the posts to the users"""
        return Posts.objects.all()
        
    
class LikeUnlikePosts(APIView):
    """for this we will use APIView, this gives us control over
    handling reqs like POST, DELETE reqs
    
    Now lets handle liking and unliking a post"""
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """for handling like posts"""
        try:
            """check if the post exist"""
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return Response({'error' : 'Posts, not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the user has already liked the posts, so as to not create a double entry
        user = request.user   #if user is authenticated

        # if the user has already liked the post
        if LikedPost.objects.filter(user=user, post=post).exists():
            # if the user has already liked the post
            return Response({'message':'you already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        # if the user hasn't, create a new LikedPost entry
        # or should i say, create a new like
        # or should i say the create a new LikedPost object to store the user that liked, and the post
        liked_post = LikedPost.objects.create(user=user, post=post)
        liked_post.save()
        return Response({'message':'post liked successfully'}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        try:
            """check if post exist, if yes, get the post"""
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return Response({'error':'post not found'}, status=status.HTTP_404_NOT_FOUND)
        user = request.user

        # now check if the user has liked the posts, if so, then delete it
        try:
            liked_post = LikedPost.objects.get(user=user, post=post)
            liked_post.delete()
            return Response({'message':'post has been un-liked'}, status=status.HTTP_200_OK)
        except LikedPost.DoesNotExist:
            return Response({'error': 'you cannot unlike because, it does not exists'}, status=status.HTTP_400_BAD_REQUEST)
            
"""get liked post class i s next, then the django class admin"""

class GetLikedPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """fetch post liked by the logged in user"""
        user = self.request.user
        liked_post = LikedPost.objects.filter(user=user).select_related('post')
        """"The select_related('post') references the entire Posts object through the post ForeignKey in LikedPost"""
        return [like.post for like in liked_post]

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


"""Now for the recommend feature"""
class Recommend:
    pass

