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
from network.models import Profile


class TestIndexViewResolution(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_login_url_is_resolved(self):
        url = reverse("login")
        print(resolve(url))
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_view)

    def test_register_url_is_resolved(self):
        url = reverse("register")
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)

    def test_newPost_url_is_resolved(self):
        url = reverse("newPost")
        print(resolve(url))
        self.assertEquals(resolve(url).func, newPost)

    def test_profile_url_is_resolved(self):
        url = reverse("profile", kwargs={"username": "test_user_made_up"})
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile)

    def test_follow_url_is_resolved(self):
        url = reverse("follow", kwargs={"username": "test_user_made_up"})
        print(resolve(url))
        self.assertEquals(resolve(url).func, follow)

    def test_unfollow_url_is_resolved(self):
        url = reverse("unfollow", kwargs={"username": "test_user_made_up"})
        print(resolve(url))
        self.assertEquals(resolve(url).func, unfollow)

    def test_following_url_is_resolved(self):
        url = reverse("following")
        print(resolve(url))
        self.assertEquals(resolve(url).func, following)

    def test_followers_url_is_resolved(self):
        url = reverse("followers")
        print(resolve(url))
        self.assertEquals(resolve(url).func, followers)

    def test_like_url_is_resolved(self):
        url = reverse("like", kwargs={"post_id": 123})
        print(resolve(url))
        self.assertEquals(resolve(url).func, like)

    def test_editPost_url_is_resolved(self):
        url = reverse("editPost")
        print(resolve(url))
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
        print(resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/index.html")

    def test_login_url_is_resolved(self):
        url = reverse("login")
        response = self.client.get(url)
        print(resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/login.html")

    def test_logout_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("logout")
        response = self.client.get(url)
        print(resolve(url))
        self.assertRedirects(response, "/")

    def test_register_url_is_resolved(self):
        url = reverse("register")
        response = self.client.get(url)
        print(resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/register.html")

    def test_newPost_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("newPost")
        response = self.client.post(url, data={"post": "Test post"})
        print(resolve(url))
        self.assertRedirects(response, "/")

    def test_profile_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("profile", kwargs={"username": "testuser"})
        response = self.client.get(url)
        print(resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/profile.html")

    def test_follow_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("follow", kwargs={"username": "testuser"})
        response = self.client.get(url)
        print(resolve(url))
        self.assertRedirects(response, "/profile/testuser")

    def test_unfollow_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("unfollow", kwargs={"username": "testuser"})
        response = self.client.get(url)
        print(resolve(url))
        self.assertRedirects(response, "/profile/testuser")

    def test_following_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("following")
        response = self.client.get(url)
        print(resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/following.html")

    def test_followers_url_is_resolved(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpass")

        url = reverse("followers")
        response = self.client.get(url)
        print(resolve(url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/followers.html")

    # @patch("network.views.Post")
    # def test_like_url_is_resolved(self, mock_post):
    #     # Set the behavior of the Post.objects.get method to raise a DoesNotExist exception
    #     mock_post.DoesNotExist = ObjectDoesNotExist
    #     mock_post.objects.get.side_effect = ObjectDoesNotExist

    #     # Log in the test user
    #     self.client.login(username="testuser", password="testpass")

    #     url = reverse("like", kwargs={"post_id": 10})
    #     response = self.client.get(url)
    #     print(resolve(url))
    #     self.assertRedirects(response, "/")

    # def test_editPost_url_is_resolved(self):
    #     # Log in the test user
    #     self.client.login(username="testuser", password="testpass")

    #     url = reverse("editPost")
    #     response = self.client.get(url)
    #     print(resolve(url))
    #     self.assertEqual(response.status_code, 200)
