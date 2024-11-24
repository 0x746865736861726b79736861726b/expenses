from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from ..models import Expenses
from .serializers import (
    ExpensesSerializer,
    ExpenseFilterSerializer,
    ExpensesSummarySerializer,
    ExpensesSummaryResponseSerializer,
)


class ExpensesViewSet(ModelViewSet):
    queryset = Expenses.objects.select_related("user").all()
    serializer_class = ExpensesSerializer

    def get_serializer_class(self):
        """
        Return the serializer class for the given action.

        Depending on the action, returns the class of the serializer to use.

        :return: The serializer class to use.
        """
        if self.action == "filter_expenses":
            return ExpenseFilterSerializer
        elif self.action == "summary":
            return ExpensesSummarySerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["post"], url_path="filter")
    def filter_expenses(self, request):
        """
        Filter expenses by user_id and date range.

        Args:
            request (Request): request object

        Returns:
            Response: response object with filtered expenses
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            expenses = serializer.get_expenses()
            return Response(ExpensesSerializer(expenses, many=True).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="summary")
    def summary(self, request):
        """
        Get the total expenses per category for a user in a given month.

        Args:
            request (Request): request object

        Returns:
            Response: response object with total expenses per category
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            summary = serializer.get_summary()
            return Response(ExpensesSummaryResponseSerializer(summary, many=True).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
