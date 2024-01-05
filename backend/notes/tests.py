from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from notes.models import Notes
from rest_framework.authtoken.models import Token


class NotesTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.notes = Notes.objects.create(
            created_by=self.user, title="Note1", description="This is note 1"
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_notes(self):
        url = "/api/notes/"

        response = self.client.get(url, format="json")

        print("Testing Get Notes List")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = f"/api/notes/{self.notes.id}/"
        data = {"title": "Note10", "description": "Note 9 is created"}
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        url = f"/api/notes/{self.notes.id}/"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteTestPost(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_post_note(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        url = "/api/notes/"
        data = {"title": "Note9", "description": "Note 9 is created"}
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        note = Notes.objects.all()[0].title
        self.assertEqual(note, "Note9")
