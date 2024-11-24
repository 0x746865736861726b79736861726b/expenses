import uuid

from rest_framework import serializers

from ..models import Expenses
from ..selectors.expenses import ExpensesSelector
from .validators import validate_uuid4, validate_user_exists


class ExpensesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Expenses
        fields = ["id", "user", "title", "amount", "date", "category"]
        read_only_fields = ["id"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be positive.")
        return value


class ExpenseFilterSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(
        required=True, validators=[validate_uuid4, validate_user_exists]
    )
    start_date = serializers.DateField(required=True, format="%Y-%m-%d")
    end_date = serializers.DateField(required=True, format="%Y-%m-%d")

    class Meta:
        fields = ["user_id", "start_date", "end_date"]

    def validate(self, data):
        """
        Ensure the start date is before the end date.
        """
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("Start date must be before end date.")
        return data

    def get_expenses(self):
        """
        Return a QuerySet of expenses for the given user and date range.

        :return: QuerySet of expenses
        """
        return ExpensesSelector.list_expenses_by_date_range(
            user_id=self.validated_data["user_id"],
            start_date=self.validated_data["start_date"],
            end_date=self.validated_data["end_date"],
        )


class ExpensesSummarySerializer(serializers.Serializer):
    user_id = serializers.UUIDField(
        required=True, validators=[validate_uuid4, validate_user_exists]
    )
    month = serializers.IntegerField(required=True, min_value=1, max_value=12)

    class Meta:
        fields = ["user_id", "month"]

    def validate(self, data):
        """
        Ensure the month is a valid number between 1 and 12.
        """
        if not (1 <= data["month"] <= 12):
            raise serializers.ValidationError("Month must be between 1 and 12.")
        return data

    def get_summary(self):
        """
        Retrieve the total expenses per category for a user in a specified month.

        Utilizes the `ExpensesSelector.get_category_summary` method to fetch
        a summary of expenses categorized and totaled for the given user ID
        and month.

        :return: QuerySet with category and total amount of expenses.
        """
        return ExpensesSelector.get_category_summary(
            user_id=self.validated_data["user_id"],
            month=self.validated_data["month"],
        )


class ExpensesSummaryResponseSerializer(serializers.Serializer):
    category = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
