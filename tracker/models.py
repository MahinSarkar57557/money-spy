from django.db import models
from django.contrib.auth.models import User
import datetime

# বাংলাদেশি স্টুডেন্ট ও লাইফস্টাইলের জন্য ক্যাটাগরি এবং আইকন লিস্ট
ICON_CHOICES = [
    ('fas fa-utensils', 'Food / Mess Meal'),
    ('fas fa-coffee', 'Tea & Snacks / Cafeteria'),
    ('fas fa-shopping-basket', 'Groceries / Bazar'),
    ('fas fa-book', 'Books & Study Materials'),
    ('fas fa-graduation-cap', 'Tuition Fee'),
    ('fas fa-print', 'Printing & Stationery'),
    ('fas fa-bus', 'Local Bus / Transport'),
    ('fas fa-motorcycle', 'Rickshaw / CNG Fare'),
    ('fas fa-plane', 'Tour & Traveling'),
    ('fas fa-home', 'Mess Rent / House Rent'),
    ('fas fa-bolt', 'Electricity Bill'),
    ('fas fa-wifi', 'Internet & Wi-Fi'),
    ('fas fa-mobile-alt', 'Mobile Recharge'),
    ('fas fa-tshirt', 'Clothing / Shopping'),
    ('fas fa-medkit', 'Medical / Pharmacy'),
    ('fas fa-film', 'Entertainment & Movies'),
    ('fas fa-gift', 'Gifts & Daan'),
    ('fas fa-futbol', 'Sports & Gym'),
    ('fas fa-wallet', 'Pocket Money / Salary'),
    ('fas fa-university', 'Scholarship / Bank')
]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="ক্যাটাগরির নাম")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-utensils', verbose_name="আইকন")
    color = models.CharField(max_length=20, default='#16a085', verbose_name="কালার কোড")
    is_income = models.BooleanField(default=False, verbose_name="আয় ক্যাটাগরি কি?")

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'আয়'),
        ('expense', 'খরচ')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="শিরোনাম")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="পরিমাণ (টাকা)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="ক্যাটাগরির")
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
        unique_together = ('user', 'category', 'month', 'year') # একই মাসে একই ক্যাটাগরিতে বারবার বাজেট যেন না হয়
        verbose_name = "বাজেট"
        verbose_name_plural = "বাজেটসমূহ"

    def __str__(self):
        return f"{self.category.name} - ৳{self.amount} ({self.month}/{self.year})"