from uuid import uuid4
from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import User
from expenses.models import Expenses


class ExpensesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid4(),
            username="testuser",
            email="testuser@example.com",
        )

        self.expense = Expenses.objects.create(
            user=self.user,
            title="Test Expense",
            amount=100.00,
            date=date(2024, 11, 24),
            category="Food",
        )

    def test_expense_creation(self):
        self.assertEqual(self.expense.title, "Test Expense")
        self.assertEqual(self.expense.amount, 100.00)
        self.assertEqual(self.expense.category, "Food")
        self.assertEqual(self.expense.user, self.user)

    def test_expense_str_representation(self):
        self.assertEqual(str(self.expense), "Test Expense - 100.0 (Food)")

    def test_date_filter(self):
        expenses = Expenses.objects.filter(date__year=2024, date__month=11)
        self.assertIn(self.expense, expenses)

    def test_negative_amount(self):
        with self.assertRaises(ValidationError):
            expense = Expenses(
                user=self.user,
                title="Invalid Expense",
                amount=-50.00,
                date=date(2024, 11, 24),
                category="Misc",
            )
            expense.clean()
