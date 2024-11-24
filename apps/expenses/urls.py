from django.urls import path
from rest_framework.routers import DefaultRouter

from .api.viewsets import ExpensesViewSet

router = DefaultRouter()
router.register(r"", ExpensesViewSet, basename="expenses")

urlpatterns = router.urls
