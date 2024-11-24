import uuid

from django.db.models import QuerySet, Sum

from ..models import Expenses


class ExpensesSelector:
    @staticmethod
    def _filter_expenses(user_id: uuid.UUID, **filters) -> QuerySet:
        """
        A reusable filtering method for expenses.

        :param user_id: ID of the user.
        :param filters: Additional filters to apply (e.g., date range, category).
        :return: Filtered QuerySet of expenses.
        """
        return Expenses.objects.filter(user_id=user_id, **filters).select_related(
            "user"
        )

    @staticmethod
    def list_expenses_by_user(user_id: uuid.UUID) -> QuerySet:
        """
        Fetch all expenses for a specific user.
        """
        return ExpensesSelector._filter_expenses(user_id)

    @staticmethod
    def list_expenses_by_date_range(
        user_id: uuid.UUID, start_date: str, end_date: str
    ) -> QuerySet:
        """
        Fetch expenses for a user within a specific date range.
        """
        return ExpensesSelector._filter_expenses(
            user_id, date__range=[start_date, end_date]
        )

    @staticmethod
    def get_category_summary(user_id: uuid.UUID, month: int) -> QuerySet:
        """
        Calculate the total expenses per category for a user in a given month.

        :param user_id: ID of the user.
        :param month: Month to filter expenses.
        :return: QuerySet with category and total amount.
        """
        return (
            ExpensesSelector._filter_expenses(user_id, date__month=month)
            .values("category")
            .annotate(total_amount=Sum("amount"))
        )
