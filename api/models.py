from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.URLField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    externalUrl = models.URLField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.title
    
class LikedPost(models.Model):
    """tracks the posts liked by the user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    # the foreign key helps us to identify the user who liked the post
    # the on_Delete ensures that if a user is deleted, their likes are also removed
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='liked')
    # the foreign key helps us to identify which post was liked
    # on_delete means if a post is deleted, all associated likes are also deleted

    # class Meta:
    #     unique_together = ('user', 'post')

