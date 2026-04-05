from django.db import models
from django.conf import settings


class TransactionType(models.TextChoices):
    INCOME  = 'income',  'Income'
    EXPENSE = 'expense', 'Expense'


class Category(models.TextChoices):
    SALARY     = 'salary',     'Salary'
    FOOD       = 'food',       'Food'
    TRANSPORT  = 'transport',  'Transport'
    HEALTHCARE = 'healthcare', 'Healthcare'
    EDUCATION  = 'education',  'Education'
    SHOPPING   = 'shopping',   'Shopping'
    UTILITIES  = 'utilities',  'Utilities'
    INVESTMENT = 'investment', 'Investment'
    OTHER      = 'other',      'Other'


class FinancialRecord(models.Model):

    user        = models.ForeignKey(
                      settings.AUTH_USER_MODEL,
                      on_delete=models.CASCADE,
                      related_name='records'
                  )
    amount      = models.DecimalField(max_digits=15, decimal_places=2)
    type        = models.CharField(
                      max_length=10,
                      choices=TransactionType.choices
                  )
    category    = models.CharField(
                      max_length=20,
                      choices=Category.choices,
                      default=Category.OTHER
                  )
    date        = models.DateField()
    notes       = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    deleted_at  = models.DateTimeField(null=True, blank=True)  # soft delete

    class Meta:
        db_table  = 'financial_records'
        ordering  = ['-date', '-created_at']

    def __str__(self):
        return f'{self.type} | {self.amount} | {self.date}'

    @property
    def is_deleted(self):
        return self.deleted_at is not None