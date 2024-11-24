from django.contrib import admin

from .models import Expenses


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "amount", "category", "date")


admin.site.register(Expenses, ExpensesAdmin)
