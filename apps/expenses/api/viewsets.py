from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..models import Expenses
from ..filters import ExpensesFilter
from .serializers import (
    ExpensesSerializer,
    ExpenseFilterSerializer,
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

    # @action(detail=False, methods=["post"], url_path="summary")
    # def summary(self, request):
    #     """
    #     Get the total expenses per category for a user in a given month.

    #     Args:
    #         request (Request): request object

    #     Returns:
    #         Response: response object with total expenses per category
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         summary = serializer.get_summary()
    #         return Response(ExpensesSummaryResponseSerializer(summary, many=True).data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
