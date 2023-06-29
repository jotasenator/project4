# python manage.py test  network.tests.test_models
from django.test import TestCase
from django.contrib.auth import get_user_model
from network.models import Post, Profile


class PostTestCase(TestCase):
    def setUp(self):
        # Get the custom user model
        User = get_user_model()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Create a post for the test user
        self.post = Post.objects.create(user=self.user, text="Test post")

    def test_post_creation(self):
        self.assertEqual(self.post.user.username, "testuser")
        self.assertEqual(self.post.text, "Test post")
        self.assertEqual(self.post.likes.count(), 0)

    def test_post_like(self):
        self.post.likes.add(self.user)
        self.assertEqual(self.post.likes.count(), 1)


class ProfileTestCase(TestCase):
    def setUp(self):
        # Get the custom user model
        User = get_user_model()

        # Create test users
        self.user1 = User.objects.create_user(username="testuser1", password="testpass")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass")

        # Create profiles for the test users
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

    def test_followers(self):
        # Test adding a follower
        self.profile2.followers.add(self.user1)
        self.assertEqual(self.profile2.followers.count(), 1)
        self.assertEqual(self.profile2.followers.first(), self.user1)

        # Test removing a follower
        self.profile2.followers.remove(self.user1)
        self.assertEqual(self.profile2.followers.count(), 0)

    def test_following(self):
        # Test adding a following
        self.profile1.following.add(self.user2)
        self.assertEqual(self.profile1.following.count(), 1)
        self.assertEqual(self.profile1.following.first(), self.user2)

        # Test removing a following
        self.profile1.following.remove(self.user2)
        self.assertEqual(self.profile1.following.count(), 0)
