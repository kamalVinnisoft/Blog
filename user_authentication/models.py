from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    profile_pic = models.ImageField(upload_to='media',blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)


    def __str__(self):
        return self.email
    

class UserFollowingRequest(models.Model):
    requested_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="requested_by")
    requested_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="requested_to")
    accepted=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.requested_by.username} -> {self.requested_to.username}"

    class Meta:
        verbose_name = "User Following Request"
        verbose_name_plural = "User Following Requests"
        unique_together = ("requested_by", "requested_to")

