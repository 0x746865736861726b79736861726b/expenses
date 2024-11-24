from uuid import uuid4
from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from expenses.models import Expenses


class ExpensesViewSetTest(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a user and an expense for that user, as
        well as an APIClient instance to make requests to the API.
        """
        self.user = User.objects.create(
            id=uuid4(),
            username="testuser",
            email="testuser@example.com",
        )

        self.expense = Expenses.objects.create(
            user=self.user,
            title="Groceries",
            amount=50.00,
            date=date(2024, 11, 1),
            category="Food",
        )

        self.client = APIClient()

    def test_create_expense(self):
        """
        Test creating an expense returns a 201 status code and the created expense
        object with the title 'Utilities'.
        """
        url = "/api/"
        data = {
            "user": str(self.user.id),
            "title": "Utilities",
            "amount": 100.00,
            "date": "2024-11-05",
            "category": "Utilities",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["title"], "Utilities")

    def test_filter_expenses(self):
        """
        Test filtering expenses by user and date range returns a list of
        expenses and the status code is 200.
        """
        url = "/api/filter/"
        data = {
            "user_id": str(self.user.id),
            "start_date": "2024-11-01",
            "end_date": "2024-11-30",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Groceries")

    def test_summary(self):
        """
        Test getting the total expenses per category for a user in a given month
        returns a list of categories with total amounts and the status code is 200.
        """
        url = "/api/summary/"
        data = {
            "user_id": str(self.user.id),
            "month": 11,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["category"], "Food")
        self.assertEqual(response.data[0]["total_amount"], "50.00")

    def test_invalid_filter_expenses(self):
        """
        Test filtering expenses with invalid data returns a 400 status code and
        "non_field_errors" in the response data.
        """
        url = "/api/filter/"
        data = {
            "user_id": str(self.user.id),
            "start_date": "2024-11-30",
            "end_date": "2024-11-01",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_invalid_summary(self):
        url = "/api/summary/"
        data = {
            "user_id": str(self.user.id),
            "month": 13,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("month", response.data)
