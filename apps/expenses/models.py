from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class Expenses(BaseModel):
    CATEGORY_CHOICES = [
        ("food", _("Food")),
        ("travel", _("Travel")),
        ("utilities", _("Utilities")),
    ]
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    class Meta:
        db_table = "expenses"
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.category})"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError(_("Expense amount must be positive"))
