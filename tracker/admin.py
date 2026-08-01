from django.contrib import admin
from .models import Transaction, Budget

# ট্রানজ্যাকশন এবং বাজেট এডমিন প্যানেলে রেজিস্টার করা হলো
admin.site.register(Transaction)
admin.site.register(Budget)