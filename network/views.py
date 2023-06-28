from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile

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
    followers = profile_user.following.count()
    followings = profile_user.followers.count()
    posts = Post.objects.filter(user=profile_user).order_by("-created_at")

    is_following = False
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        is_following = profile.following.filter(id=profile_user.id).exists()

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


@login_required
def follow(request, username):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_user = User.objects.get(username=username)
    profile.following.add(profile_user)
    profile_user.profile.followers.add(request.user)
    return HttpResponseRedirect(reverse("profile", args=[username]))


@login_required
def unfollow(request, username):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_user = User.objects.get(username=username)
    profile.following.remove(profile_user)
    profile_user.profile.followers.remove(request.user)
    return HttpResponseRedirect(reverse("profile", args=[username]))


def following(request):
    following = request.user.profile.following.all()
    allPosts = Post.objects.all().filter(user__in=following).order_by("-created_at")
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"page_obj": page_obj})


def followers(request):
    followers = request.user.profile.followers.all()
    return render(request, "network/followers.html", {"followers": followers})
