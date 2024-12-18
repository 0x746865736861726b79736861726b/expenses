from uuid import uuid4
from datetime import date

from django.test import TestCase

from users.models import User
from expenses.models import Expenses
from expenses.selectors.expenses import ExpensesSelector


class ExpensesSelectorTest(TestCase):
    def setUp(self):
        """
        Create a test user and three expenses for that user.

        The three expenses are:
        - Groceries (Food, 50.00, 2024-11-01)
        - Transport (Travel, 20.00, 2024-11-15)
        - Utilities (Utilities, 100.00, 2024-10-30)
        """
        self.user = User.objects.create(
            id=uuid4(),
            username="testuser",
            email="testuser@example.com",
        )

        self.expense1 = Expenses.objects.create(
            user=self.user,
            title="Groceries",
            amount=50.00,
            date=date(2024, 11, 1),
            category="Food",
        )
        self.expense2 = Expenses.objects.create(
            user=self.user,
            title="Transport",
            amount=20.00,
            date=date(2024, 11, 15),
            category="Travel",
        )
        self.expense3 = Expenses.objects.create(
            user=self.user,
            title="Utilities",
            amount=100.00,
            date=date(2024, 10, 30),
            category="Utilities",
        )

    def test_list_expenses_by_user(self):
        """
        Tests that list_expenses_by_user returns all expenses for a given user.

        The user created in setUp has three expenses. This test ensures that
        list_expenses_by_user returns a QuerySet with all three expenses.
        """
        expenses = ExpensesSelector.list_expenses_by_user(user_id=self.user.id)
        self.assertEqual(expenses.count(), 3)
        self.assertIn(self.expense1, expenses)
        self.assertIn(self.expense2, expenses)
        self.assertIn(self.expense3, expenses)

    def test_list_expenses_by_date_range(self):
        """
        Tests that list_expenses_by_date_range returns the correct expenses for a
        given user within a specific date range.
        """
        expenses = ExpensesSelector.list_expenses_by_date_range(
            user_id=self.user.id, start_date="2024-11-01", end_date="2024-11-30"
        )
        self.assertEqual(expenses.count(), 2)
        self.assertIn(self.expense1, expenses)
        self.assertIn(self.expense2, expenses)
        self.assertNotIn(self.expense3, expenses)

    def test_get_category_summary(self):
        """
        Tests that get_category_summary returns the expected results.

        This test verifies that:

        - The method returns a QuerySet with two items.
        - The two items have category "Food" and "Travel".
        - The total amount for the "Food" category is 50.00.
        - The total amount for the "Travel" category is 20.00.
        """
        summary = ExpensesSelector.get_category_summary(user_id=self.user.id, month=11)
        self.assertEqual(len(summary), 2)
        food_summary = next((s for s in summary if s["category"] == "Food"), None)
        travel_summary = next((s for s in summary if s["category"] == "Travel"), None)

        self.assertIsNotNone(food_summary)
        self.assertIsNotNone(travel_summary)
        self.assertEqual(food_summary["total_amount"], 50.00)
        self.assertEqual(travel_summary["total_amount"], 20.00)
