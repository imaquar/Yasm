from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timesince


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    bio = models.TextField(max_length=298, blank=True, null=True)

    @property
    def liked_posts(self):
        return self.likes_by_liker.filter(comment=None).values_list("post", flat=True)
    
    @property
    def liked_comments(self):
        return self.likes_by_liker.filter(post=None).values_list("comment", flat=True)


class Entry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    @property
    def timesince(self):
        value = str(timesince.timesince(self.datetime))
        try:
            return value[:value.index(",")]
        except ValueError:
            if value[0] != "0":
                return value
            else:
                return "just now"
    
    class Meta:
        abstract = True


class Post(Entry):
    text = models.TextField(max_length=1024)
        

class Comment(Entry):
    text = models.TextField(max_length=512)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_by_post")

    class Meta:
        ordering = ["-datetime"]
        

class Like(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name="likes_by_post")
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name="likes_by_comment")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_by_liker")
