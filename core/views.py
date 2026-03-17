from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Category, Expense, Income, Budget, Loan
from .serializers import (
    UserSerializer, CategorySerializer, ExpenseSerializer, 
    IncomeSerializer, BudgetSerializer, LoanSerializer
)
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user) | Category.objects.filter(user__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SummaryView(APIView):
    def get(self, request):
        user = request.user
        total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        loans_given = Loan.objects.filter(user=user, type='GIVEN', is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
        loans_taken = Loan.objects.filter(user=user, type='TAKEN', is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'loans_given': loans_given,
            'loans_taken': loans_taken,
            'balance': total_income - total_expense
        })

class StatisticsView(APIView):
    def get(self, request):
        user = request.user
        
        # 1. Category Breakdown (Expenses)
        category_data = Expense.objects.filter(user=user).values('category__name', 'category__color').annotate(value=Sum('amount')).order_by('-value')
        
        # 2. Monthly Trends (Last 6 Months)
        six_months_ago = timezone.now().date() - timedelta(days=180)
        
        monthly_expenses = Expense.objects.filter(user=user, date__gte=six_months_ago) \
            .annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(total=Sum('amount')) \
            .order_by('month')
            
        monthly_income = Income.objects.filter(user=user, date__gte=six_months_ago) \
            .annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(total=Sum('amount')) \
            .order_by('month')

        # Combine trends
        trends = {}
        for item in monthly_expenses:
            m = item['month'].strftime('%b %Y')
            trends[m] = trends.get(m, {'month': m, 'expense': 0, 'income': 0})
            trends[m]['expense'] = float(item['total'])
            
        for item in monthly_income:
            m = item['month'].strftime('%b %Y')
            trends[m] = trends.get(m, {'month': m, 'expense': 0, 'income': 0})
            trends[m]['income'] = float(item['total'])

        return Response({
            'categories': [{'name': item['category__name'] or 'Other', 'value': float(item['value']), 'color': item['category__color']} for item in category_data],
            'trends': sorted(trends.values(), key=lambda x: timezone.datetime.strptime(x['month'], '%b %Y').date())
        })
