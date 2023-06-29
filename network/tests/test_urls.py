# python manage.py test  network.tests.test_urls

from django.test import SimpleTestCase, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from network.views import (
    index,
    login_view,
    logout_view,
    register,
    newPost,
    profile,
    follow,
    unfollow,
    following,
    followers,
    like,
    editPost,
)
from network.models import Profile, Post


class TestIndexViewResolution(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")

        self.assertEquals(resolve(url).func, index)

    def test_login_url_is_resolved(self):
        url = reverse("login")

        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")

        self.assertEquals(resolve(url).func, logout_view)

    def test_register_url_is_resolved(self):
        url = reverse("register")

        self.assertEquals(resolve(url).func, register)

    def test_newPost_url_is_resolved(self):
        url = reverse("newPost")

        self.assertEquals(resolve(url).func, newPost)

    def test_profile_url_is_resolved(self):
        url = reverse("profile", kwargs={"username": "test_user_made_up"})

        self.assertEquals(resolve(url).func, profile)

    def test_follow_url_is_resolved(self):
        url = reverse("follow", kwargs={"username": "test_user_made_up"})

        self.assertEquals(resolve(url).func, follow)

    def test_unfollow_url_is_resolved(self):
        url = reverse("unfollow", kwargs={"username": "test_user_made_up"})

        self.assertEquals(resolve(url).func, unfollow)

    def test_following_url_is_resolved(self):
        url = reverse("following")

        self.assertEquals(resolve(url).func, following)

    def test_followers_url_is_resolved(self):
        url = reverse("followers")

        self.assertEquals(resolve(url).func, followers)

    def test_like_url_is_resolved(self):
        url = reverse("like", kwargs={"post_id": 123})

        self.assertEquals(resolve(url).func, like)

    def test_editPost_url_is_resolved(self):
        url = reverse("editPost")

        self.assertEquals(resolve(url).func, editPost)


class TestIndexView(TestCase):
    def setUp(self):
        # Get the custom user model
        User = get_user_model()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create a profile for the test user
        Profile.objects.create(user=self.user)

    def test_index_url_is_resolved(self):
        url = reverse("index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/index.html")

    def test_login_url_is_resolved(self):
        url = reverse("login")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/login.html")

    def test_logout_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("logout")
        response = self.client.get(url)

        self.assertRedirects(response, "/")

    def test_register_url_is_resolved(self):
        url = reverse("register")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/register.html")

    def test_newPost_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("newPost")
        response = self.client.post(url, data={"post": "Test post"})

        self.assertRedirects(response, "/")

    def test_profile_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("profile", kwargs={"username": "testuser"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/profile.html")

    def test_follow_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("follow", kwargs={"username": "testuser"})
        response = self.client.get(url)

        self.assertRedirects(response, "/profile/testuser")

    def test_unfollow_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("unfollow", kwargs={"username": "testuser"})
        response = self.client.get(url)

        self.assertRedirects(response, "/profile/testuser")

    def test_following_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("following")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/following.html")

    def test_followers_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("followers")
        response = self.client.get(url)
        (resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/followers.html")

    def test_like_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        # Create a test post
        post = Post.objects.create(user=self.user, text="Test post")
        # PK of the Post object I've created above
        post_id = post.id

        url = reverse("like", args=[post_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # fun fact, by doing this test I could see I had an error on my editPost function
    # I was editing but not saving the post, so after refreshing the page the edit was lost :)

    def test_editPost_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        # Create a test post
        post = Post.objects.create(user=self.user, text="old post")
        # PK of the Post object I've created above
        post_id = post.id

        url = reverse("editPost")
        data = {"post_text": "new post", "post_id": post_id}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Check that the post text has been updated
        updated_post = Post.objects.get(id=post_id)
        self.assertEqual(updated_post.text, "new post")
