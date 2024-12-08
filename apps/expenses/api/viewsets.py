from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..models import Expenses
from ..filters import ExpensesFilter
from ..selectors.expenses import ExpensesSelector
from .serializers import (
    ExpensesSerializer,
    ExpensesSummarySerializer,
    ExpensesSummaryResponseSerializer,
)


class ExpensesViewSet(ModelViewSet):
    queryset = Expenses.objects.select_related("user").all()
    serializer_class = ExpensesSerializer
    permission_classes = [AllowAny]
    filterset_class = ExpensesFilter

    def get_queryset(self):
        """
        Optionally restricts the returned expenses to a user-filtered query,
        by filtering against query parameters in the request.
        """
        queryset = super().get_queryset()
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Overrides the default `list` method to apply filtering and optionally provide summaries.
        """
        if request.query_params.get("summary"):
            serializer = ExpensesSummaryResponseSerializer(
                self.get_summary_data(), many=True
            )
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def get_summary_data(self):
        """
        Retrieve summary data (total expenses per category) for a user in a specified month.
        """
        user_id = self.request.query_params.get("user_id")
        month = self.request.query_params.get("month")

        if not user_id or not month:
            raise serializers.ValidationError(
                {
                    "error": "Both 'user_id' and 'month' query parameters are required for a summary."
                }
            )

        return ExpensesSelector.get_category_summary(user_id=user_id, month=month)
