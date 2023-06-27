from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator


def index(request):
    allPosts = Post.objects.all().order_by("-created_at")
    # allPosts = Post.objects.all().order_by("created_at").reverse()
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj})


@login_required
def newPost(request):
    if request.method == "POST":
        text = request.POST["post"]
        user = User.objects.get(pk=request.user.id)
        post = Post(user=user, text=text)
        post.save()
        return HttpResponseRedirect(reverse("index"))


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    profile_user = User.objects.get(username=username)
    followers = profile_user.followers.count()
    followings = profile_user.following.count()
    posts = Post.objects.filter(user=profile_user).order_by("-created_at")

    is_following = False
    if request.user.is_authenticated:
        is_following = profile_user.followers.filter(id=request.user.id).exists()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/profile.html",
        {
            "profile_user": profile_user,
            "followers": followers,
            "followings": followings,
            "page_obj": page_obj,
            "is_following": is_following,
        },
    )
