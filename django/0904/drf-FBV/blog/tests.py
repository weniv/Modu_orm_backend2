from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post


class BlogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post content", author=self.user
        )

    def test_get_post_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)

    def test_get_post_list_unauthenticated(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 401)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Test Post", "content": "This is a new test post content"}
        response = self.client.post("/blog/", data)
        self.assertEqual(response.status_code, 201)

    def test_create_post_unauthenticated(self):
        data = {"title": "New Test Post", "content": "This is a new test post content"}
        response = self.client.post("/blog/", data)
        self.assertEqual(response.status_code, 401)

    def test_get_post_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/blog/{self.post.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_post_author(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Test Post",
            "content": "This is an updated test post content",
        }
        response = self.client.put(f"/blog/{self.post.id}/", data)
        self.assertEqual(response.status_code, 200)

    def test_update_post_non_author(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpassword123"
        )
        self.client.force_authenticate(user=other_user)
        data = {
            "title": "Updated Test Post",
            "content": "This is an updated test post content",
        }
        response = self.client.put(f"/blog/{self.post.id}/", data)
        self.assertEqual(response.status_code, 403)

    def test_delete_post_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/blog/{self.post.id}/")
        self.assertEqual(response.status_code, 204)

    def test_delete_post_non_author(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpassword123"
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(f"/blog/{self.post.id}/")
        self.assertEqual(response.status_code, 403)
