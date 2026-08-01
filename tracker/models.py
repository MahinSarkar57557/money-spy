from django.db import models
from django.contrib.auth.models import User
import datetime

# ফিক্সড ২৯টি ক্যাটাগরির লিস্ট (যা ডাটাবেজে স্ট্রিং হিসেবে সেভ হবে)
CATEGORY_CHOICES = [
    ('Tuition & Fees', 'Tuition & Fees'),
    ('Books & Notes', 'Books & Notes'),
    ('Stationery', 'Stationery'),
    ('Courses & Training', 'Courses & Training'),
    ('Mess / Hall Bill', 'Mess / Hall Bill'),
    ('Restaurants & Fast Food', 'Restaurants & Fast Food'),
    ('Tea & Snacks', 'Tea & Snacks'),
    ('Groceries', 'Groceries'),
    ('Bus / Local Transport', 'Bus / Local Transport'),
    ('Rickshaw & CNG', 'Rickshaw & CNG'),
    ('Bike Fuel / Maintenance', 'Bike Fuel / Maintenance'),
    ('Tour & Travel', 'Tour & Travel'),
    ('Rent / Room Rent', 'Rent / Room Rent'),
    ('Electricity & Gas', 'Electricity & Gas'),
    ('Internet & WiFi', 'Internet & WiFi'),
    ('Mobile Recharge', 'Mobile Recharge'),
    ('bKash / Nagad', 'bKash / Nagad'),
    ('Clothing & Tailoring', 'Clothing & Tailoring'),
    ('Personal Care', 'Personal Care'),
    ('Medicine & Health', 'Medicine & Health'),
    ('Gym & Sports', 'Gym & Sports'),
    ('Entertainment & Subscriptions', 'Entertainment & Subscriptions'),
    ('Gift', 'Gift'),
    ('Donation', 'Donation'),
    ('Debt Repayment', 'Debt Repayment'),
    ('Tech & Gadgets', 'Tech & Gadgets'),
    ('Savings & Investment', 'Savings & Investment'),
    ('Miscellaneous / Others', 'Miscellaneous / Others'),
]

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'আয়'),
        ('expense', 'খরচ')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="শিরোনাম")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="পরিমাণ (টাকা)")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name="ক্যাটাগরি")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='expense', verbose_name="ধরণ")
    date = models.DateField(default=datetime.date.today, verbose_name="তারিখ")
    description = models.TextField(blank=True, null=True, verbose_name="নোট বা বিবরণ")

    def __str__(self):
        return f"{self.category} - {self.amount} Taka"

    class Meta:
        ordering = ['-date', '-id']


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="ব্যবহারকারী")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name="ক্যাটাগরি")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="বাজেটের পরিমাণ (টাকা)")
    month = models.IntegerField(verbose_name="মাস")
    year = models.IntegerField(verbose_name="বছর")

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')
        verbose_name = "বাজেট"
        verbose_name_plural = "বাজেটসমূহ"

    def __str__(self):
        return f"{self.category} - ৳{self.amount} ({self.month}/{self.year})"