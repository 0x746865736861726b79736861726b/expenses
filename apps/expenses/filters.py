import django_filters

from .models import Expenses


class ExpensesFilter(django_filters.FilterSet):
    user_id = django_filters.UUIDFilter(field_name="user_id", lookup_expr="exact")
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Expenses
        fields = ["user_id", "start_date", "end_date"]
