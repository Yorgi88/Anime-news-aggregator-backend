from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Posts, LikedPost


class UserSerializer(serializers.ModelSerializer):
    # to repr a user
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password' : {'write_only': True}}
        # accepting a password when creating a user, but the  password gets hidden when we want info about the user

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()  #adding a custom field for the like status
    class Meta:
        model = Posts
        fields = ['id', 'img', 'title', 'description', 'externalUrl', 'liked']

    def get_liked(self, obj):
        """if the user is authenticated
         and if there is a corresponding entry in the liked post table where, user matches the logged in user
        post matches the current post being serialized
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LikedPost.objects.filter(user=request.user, post=obj).exists()
        return False
        



# class LikedPostSerializer(serializers.ModelSerializer):
#     post = PostSerializer()

#     class Meta:
#         model = LikedPost
#         fields = ['id','post']

# class CreateLikedPostSerializer(serializers.ModelSerializer):
#     """we need to store the post details in which the user has liked"""
#     class Meta:
#         models = LikedPost
#         fields = ['post']

