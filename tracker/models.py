from django.db import models
from django.contrib.auth.models import User
import datetime

# ক্যাটাগরি আইকন লিস্ট (এক্সপেন্স এবং ইনকাম উভয়ের জন্য)
ICON_CHOICES = [
    # Expense Icons
    ('fas fa-utensils', 'Food & Snacks'),
    ('fas fa-bus', 'Transport & Commute'),
    ('fas fa-home', 'Rent & Mess Bill'),
    ('fas fa-bolt', 'Utilities (Gas/Electricity)'),
    ('fas fa-wifi', 'Internet & Mobile'),
    ('fas fa-book', 'Study & Stationery'),
    ('fas fa-graduation-cap', 'University Fee'),
    ('fas fa-chalkboard-teacher', 'Tuition & Coaching'),
    ('fas fa-shopping-bag', 'Shopping'),
    ('fas fa-cut', 'Hair Cut & Grooming'),
    ('fas fa-medkit', 'Health & Medical'),
    ('fas fa-gift', 'Gifts & Donation'),
    ('fas fa-coffee', 'Tea & Coffee'),
    ('fas fa-tshirt', 'Laundry & Iron'),
    ('fas fa-film', 'Entertainment & Movies'),
    ('fas fa-plane', 'Tour & Travel'),
    ('fas fa-wallet', 'bKash / Nagad Cashout'),
    ('fas fa-hand-holding-usd', 'Debt Repayment'),
    ('fas fa-piggy-bank', 'Savings & Deposit'),
    ('fas fa-shield-alt', 'Emergency Fund'),
    ('fas fa-ellipsis-h', 'Other Expenses'),
    
    # Income Icons
    ('fas fa-laptop-code', 'Freelancing'),
    ('fas fa-briefcase', 'Job Salary'),
    ('fas fa-award', 'Scholarship'),
    ('fas fa-book-reader', 'Tuition Income'),
    ('fas fa-coins', 'Pocket Money'),
    ('fas fa-store', 'Business Income'),
    ('fas fa-shopping-cart', 'Online Sales'),
    ('fas fa-chart-line', 'Investment'),
    ('fas fa-hand-holding-heart', 'Dividend / Profit'),
    ('fas fa-undo-alt', 'Money Back / Return'),
    ('fas fa-plus-circle', 'Other Income')
]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="ক্যাটাগরির নাম")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-utensils', verbose_name="আইকন")
    color = models.CharField(max_length=20, default='#16a085', verbose_name="কালার কোড")
    is_income = models.BooleanField(default=False, verbose_name="আয় ক্যাটাগরি কি? (True হলে ইনকাম, False হলে খরচ)")

    def __str__(self):
        cat_type = "Income" if self.is_income else "Expense"
        return f"{self.name} ({cat_type})"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'আয়'),
        ('expense', 'খরচ')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="শিরোনাম")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="পরিমাণ (টাকা)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="ক্যাটাগরি")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='expense', verbose_name="ধরণ")
    date = models.DateField(default=datetime.date.today, verbose_name="তারিখ")
    description = models.TextField(blank=True, null=True, verbose_name="নোট বা বিবরণ")

    def __str__(self):
        if self.category:
            return f"{self.category.name} - {self.amount} Taka"
        return f"Transaction - {self.amount} Taka"

    class Meta:
        ordering = ['-date', '-id']


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="ব্যবহারকারী")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="ক্যাটাগরি")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="বাজেটের পরিমাণ (টাকা)")
    month = models.IntegerField(verbose_name="মাস")
    year = models.IntegerField(verbose_name="বছর")

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')
        verbose_name = "বাজেট"
        verbose_name_plural = "বাজেটসমূহ"

    def __str__(self):
        return f"{self.category.name} - ৳{self.amount} ({self.month}/{self.year})"