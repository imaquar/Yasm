from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like, Comment
from .forms import PostForm, CommentForm, UserForm, UserUpdateForm

import ast


def index(request):
    
    # Set the forms for the case of a POST request
    post_form = PostForm(request.POST or None) 
    comment_form = CommentForm(request.POST or None)

    # Pagination
    p = Paginator(Post.objects.order_by("-datetime"), 10)
    page = request.GET.get("page")
    posts = p.get_page(page)

    if request.method == "POST":
        try:
            if "post" in request.POST:
                comment_form.instance.author = User.objects.get(pk=request.user.id)
                if comment_form.is_valid():
                    comment_form.save()
            else:
                post_form.instance.author = User.objects.get(pk=request.user.id)
                if post_form.is_valid():
                    post_form.save()

            return HttpResponseRedirect("/")
        except User.DoesNotExist:
            return redirect("login")
           
    context = {"post_form": post_form, "comment_form": comment_form, "posts": posts }

    return render(request, "network/index.html", context)


def profile(request, user_id):
    req_user = User.objects.get(pk=user_id)
    comment_form = CommentForm(request.POST or None)
    user_update_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=req_user)

    # Pagination
    p = Paginator(Post.objects.filter(author=req_user).order_by("-datetime"), 10)
    page = request.GET.get("page")
    posts = p.get_page(page)

    if request.method == "POST":
        if "text" in request.POST:
            comment_form.instance.author = User.objects.get(pk=request.user.id)
            if comment_form.is_valid():
                comment_form.save()
        elif user_update_form.is_valid():
            user_update_form.save()
    
        return HttpResponseRedirect(f"/profile/{user_id}")

    context = {
        "req_user": req_user, "posts": posts, 
        "comment_form": comment_form, "user_update_form": user_update_form
    }

    return render(request, "network/index.html", context)


def following(request):
    user = User.objects.get(pk=request.user.id)
    authors = user.following.all()
    comment_form = CommentForm(request.POST or None)

    # Pagination
    p = Paginator(Post.objects.filter(author__in=authors), 10)
    page = request.GET.get("page")
    posts = p.get_page(page)


    if request.method == "POST":
        comment_form.instance.author = User.objects.get(pk=request.user.id)
        if comment_form.is_valid():
            comment_form.save()

    context = {"posts": posts, "comment_form": comment_form} 
    return render(request, "network/index.html", context)


def handlelike(request, entry_type, entry_id):

    try:
        liker = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return redirect("login")

    try:
        if entry_type == "post":
            post = Post.objects.get(pk=entry_id)
            like = Like.objects.get(post=post, liker=liker)
        else:
            comment = Comment.objects.get(pk=entry_id)
            like = Like.objects.get(comment=comment, liker=liker)
        like.delete()
    
    except Like.DoesNotExist:
        if entry_type == "post":
            post = Post.objects.get(pk=entry_id)
            like = Like(post=post, liker=liker)
        else:
            comment = Comment.objects.get(pk=entry_id)
            like = Like(comment=comment, liker=liker)
        like.save() 

    return JsonResponse({"message": "like altered"})


def handlefollow(request, user_id):
    follower = User.objects.get(pk=request.user.id)
    req_user = User.objects.get(pk=user_id)

    if follower in req_user.followers.all():
        req_user.followers.remove(follower)
    else:
        req_user.followers.add(follower)

    return JsonResponse({"message": "follower altered"})


def delete(request, entry_type, entry_id):
    if entry_type == "post":
        entry = Post.objects.get(pk=entry_id)
    else:
        entry = Comment.objects.get(pk=entry_id)

    if request.user == entry.author:
        entry.delete()
    else:
        return HttpResponseRedirect("/")

    return HttpResponseRedirect("/")


def edit(request, entry_type, entry_id):
    if request.method == "POST":
        POST_dict = ast.literal_eval(request.body.decode("UTF-8"))
        
        if entry_type == "post":
            entry = Post.objects.get(pk=entry_id)
        else:
            entry = Comment.objects.get(pk=entry_id)
        
        entry.text = POST_dict["text"]
        entry.save()
    else:
        return HttpResponseRedirect("/")
    
    return JsonResponse({"message": "post edited"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    user_form = UserForm(request.POST, request.FILES or None)
    
    if request.method == "POST":
        username = request.POST["username"]
        password, confirmation = request.POST["password1"], request.POST["password2"]
        if password != confirmation:
            context = {"user_form": user_form, "message": "Passwords must match."}
            return render(request, "network/register.html", context)
        elif user_form.is_valid():
            user_form.save()
            login(request, authenticate(username=username, password=password))
            return redirect(index)
    return render(request, "network/register.html", {"user_form": user_form})


def update(request, user_id):
    if request.method == "POST":
        POST_dict = ast.literal_eval(request.body.decode("UTF-8"))
        user = User.objects.get(pk=user_id)
        user.bio = POST_dict["bio"]
        user.save()
    return redirect(index)


def users(request, group, obj_id):
    if group == "followers":
        obj = User.objects.get(pk=obj_id)
        users = obj.followers.all()
    elif group == "following":
        obj = User.objects.get(pk=obj_id)
        users = obj.following.all()
    elif group == "post_likers":
        obj = Post.objects.get(pk=obj_id)
        users = [like.liker for like in obj.likes_by_post.all()] 
    else:
        obj= Comment.objects.get(pk=obj_id)
        users = [like.liker for like in obj.likes_by_comment.all()] 
    return render(request, "network/users.html", {"users": users, "obj": obj})
