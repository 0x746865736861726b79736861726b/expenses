from uuid import uuid4
from datetime import date
from decimal import Decimal

from django.test import TestCase

from users.models import User
from expenses.models import Expenses
from expenses.api.serializers import (
    ExpensesSerializer,
    ExpenseFilterSerializer,
    ExpensesSummarySerializer,
    ExpensesSummaryResponseSerializer,
)


class ExpensesSerializerTest(TestCase):
    def setUp(self):
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

    def test_expenses_serializer_valid_data(self):
        """
        Tests that ExpensesSerializer validates and saves data correctly.

        Verifies that:

        - The serializer is valid with the given data.
        - The serializer saves the data to the database correctly.
        - The saved data matches the input data.
        """
        data = {
            "user": str(self.user.id),
            "title": "Groceries",
            "amount": "50.00",
            "date": "2024-11-01",
            "category": "food",
        }
        serializer = ExpensesSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        expense = serializer.save()
        self.assertEqual(expense.title, "Groceries")
        self.assertEqual(expense.amount, Decimal("50.00"))
        self.assertEqual(expense.date, date(2024, 11, 1))
        self.assertEqual(expense.category, "food")

    def test_expenses_serializer_invalid_amount(self):
        """
        Tests that ExpensesSerializer raises an error with an invalid amount.

        Verifies that:

        - The serializer is invalid with negative amount.
        - The serializer raises an error with "Expense amount must be positive."
        """
        data = {
            "user": str(self.user.id),
            "title": "Invalid Expense",
            "amount": "-10.00",
            "date": "2024-11-01",
            "category": "Food",
        }
        serializer = ExpensesSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("amount", serializer.errors)
        self.assertEqual(
            serializer.errors["amount"][0], "Expense amount must be positive."
        )

    def test_expense_filter_serializer_valid_data(self):
        """
        Tests that ExpenseFilterSerializer accepts valid date range.

        Verifies that:

        - The serializer is valid with a valid date range.
        """
        data = {
            "user_id": str(self.user.id),
            "start_date": "2024-11-01",
            "end_date": "2024-11-30",
        }
        serializer = ExpenseFilterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_expense_filter_serializer_invalid_date_range(self):
        """
        Tests that ExpenseFilterSerializer rejects invalid date range.

        Verifies that:

        - The serializer is invalid with an invalid date range.
        - The serializer raises an error with "Start date must be before end date."
        """
        data = {
            "user_id": str(self.user.id),
            "start_date": "2024-11-30",
            "end_date": "2024-11-01",
        }
        serializer = ExpenseFilterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Start date must be before end date.",
        )

    def test_expenses_summary_serializer_valid_data(self):
        """
        Tests that ExpensesSummarySerializer validates data correctly.

        Verifies that:

        - The serializer is valid with a valid user ID and month.
        """
        data = {"user_id": str(self.user.id), "month": 11}
        serializer = ExpensesSummarySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_expenses_summary_serializer_invalid_month(self):
        """
        Tests that ExpensesSummarySerializer raises an error with an invalid month.

        Verifies that:

        - The serializer is invalid when the month is greater than 12.
        - The serializer raises an error with "Ensure this value is less than or equal to 12."
        """
        data = {"user_id": str(self.user.id), "month": 13}
        serializer = ExpensesSummarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("month", serializer.errors)
        self.assertEqual(
            serializer.errors["month"][0],
            "Ensure this value is less than or equal to 12.",
        )

    def test_expenses_summary_response_serializer(self):
        """
        Tests that ExpensesSummaryResponseSerializer validates and deserializes data correctly.

        Verifies that:

        - The serializer is valid with a valid category and total amount.
        - The serializer deserializes the total amount as a Decimal.
        """
        data = {"category": "Food", "total_amount": "150.00"}
        serializer = ExpensesSummaryResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["category"], "Food")
        self.assertEqual(serializer.validated_data["total_amount"], Decimal("150.00"))
