from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField()
    profile_pic=models.ImageField(upload_to="profile_pic")
    followers=models.ManyToManyField(User,related_name="followers")


    def followers_count(self):
        return self.followers.all().count()
    
    def followers_list(self):
        return self.followers.all()

    def __str__(self):
        return self.user.username 
    
class PostModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    caption=models.TextField()
    image=models.ImageField(upload_to="post_image")
    likes=models.ManyToManyField(User,related_name="likes")

    def likes_count(self):
        return self.likes.all().count()
    
    def likes_list(self):
        return self.likes.all()
    
    def comment_count(self):
        return CommentModel.objects.filter(post=self).count()
    

    def __str__(self):
        return self.title
    
class CommentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(PostModel,on_delete=models.CASCADE)
    comment=models.TextField()