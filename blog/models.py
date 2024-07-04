from django.db import models
from user_authentication.models import *
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='media',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class Comment(models.Model):
    c_text= models.TextField()
    comment_at = models.DateTimeField(auto_now_add=True)
    comment_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    recomment = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)

class Like(models.Model):
    liked_at =models.DateTimeField(auto_now_add=True)
    liked_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
