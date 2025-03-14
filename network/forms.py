from django.forms import ModelForm, HiddenInput, FileInput, CharField
from .models import Post, Comment, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserForm(UserCreationForm):
    first_name = CharField(max_length=18)
    username = CharField(max_length=32)

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2", "image"]


class UserUpdateForm(UserChangeForm):
    first_name = CharField(max_length=18)
    username = CharField(max_length=32)

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "image", "bio"]

        widgets = {
            "image": FileInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = ""
        self.fields["username"].label = ""
        self.fields["email"].label = ""
        self.fields["bio"].label = ""
        self.fields["image"].label = ""
    

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "post"]

    widgets = {
        "post": HiddenInput()
    }

