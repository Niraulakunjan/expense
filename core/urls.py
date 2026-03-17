from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, CategoryViewSet, ExpenseViewSet, 
    IncomeViewSet, BudgetViewSet, LoanViewSet, SummaryView, StatisticsView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'income', IncomeViewSet, basename='income')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('', include(router.urls)),
]
