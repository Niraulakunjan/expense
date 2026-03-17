from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    currency = models.CharField(max_length=10, default='USD')
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    TYPE_CHOICES = (
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXPENSE')
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('user', 'name', 'type')

    def __str__(self):
        return f"{self.name} ({self.type})"

PAYMENT_METHOD_CHOICES = (
    ('CASH', 'Cash'),
    ('ESEWA', 'eSewa'),
    ('KHALTI', 'Khalti'),
    ('SIDDHARTH_QR', 'Siddharth Bank (QR)'),
    ('GLOBAL_IME_QR', 'Global IME Bank (QR)'),
    ('CONNECT_IPS', 'Connect IPS'),
    ('OTHER', 'Other'),
)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='expenses')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.date})"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_entries')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='income_entries')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.date})"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    limit = models.DecimalField(max_digits=12, decimal_places=2)
    spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')

    def __str__(self):
        return f"{self.user.username} Budget for {self.category.name} ({self.month}/{self.year})"

from django.utils import timezone

class Loan(models.Model):
    LOAN_TYPES = (
        ('GIVEN', 'Given (Debtor)'),
        ('TAKEN', 'Taken (Creditor)'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    person_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=LOAN_TYPES)
    loan_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.person_name} - ${self.amount}"
