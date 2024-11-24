from django.test import TestCase
from django.db.utils import IntegrityError

from users.models import User


class UserModelTest(TestCase):
    def test_user_creation(self):
        """
        Tests that creating a User results in the expected values being set.
        """

        user = User.objects.create(username="testuser", email="testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_username_uniqueness(self):
        """
        Tests that creating a User with a duplicate username raises an IntegrityError.
        """
        User.objects.create(username="testuser", email="test1@example.com")
        with self.assertRaises(IntegrityError):
            User.objects.create(username="testuser", email="test2@example.com")

    def test_email_uniqueness(self):
        """
        Tests that creating a User with a duplicate email address raises an IntegrityError.
        """
        User.objects.create(username="testuser1", email="test@example.com")
        with self.assertRaises(IntegrityError):
            User.objects.create(username="testuser2", email="test@example.com")

    def test_user_string_representation(self):
        """
        Tests that the string representation of a User is the username.
        """

        user = User.objects.create(username="testuser", email="testuser@example.com")
        self.assertEqual(str(user), "testuser")
