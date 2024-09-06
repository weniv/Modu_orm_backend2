from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import PostNotice


class NoticeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.notice = PostNotice.objects.create(
            title="Test Notice",
            content="This is a test notice content",
            author=self.user,
        )

    def test_get_notice_list_anonymous(self):
        response = self.client.get("/notice/")
        self.assertEqual(response.status_code, 200)

    def test_get_notice_detail_anonymous(self):
        response = self.client.get(f"/notice/{self.notice.id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_notice_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Test Notice",
            "content": "This is a new test notice content",
        }
        response = self.client.post("/notice/", data)
        self.assertEqual(response.status_code, 201)

    def test_create_notice_unauthenticated(self):
        data = {
            "title": "New Test Notice",
            "content": "This is a new test notice content",
        }
        response = self.client.post("/notice/", data)
        self.assertEqual(response.status_code, 403)

    def test_update_notice_author(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Test Notice",
            "content": "This is an updated test notice content",
        }
        response = self.client.put(f"/notice/{self.notice.id}/", data)
        self.assertEqual(response.status_code, 200)

    def test_update_notice_non_author(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpassword123"
        )
        self.client.force_authenticate(user=other_user)
        data = {
            "title": "Updated Test Notice",
            "content": "This is an updated test notice content",
        }
        response = self.client.put(f"/notice/{self.notice.id}/", data)
        self.assertEqual(response.status_code, 403)

    def test_delete_notice_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/notice/{self.notice.id}/")
        self.assertEqual(response.status_code, 204)

    def test_delete_notice_non_author(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpassword123"
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(f"/notice/{self.notice.id}/")
        self.assertEqual(response.status_code, 403)
