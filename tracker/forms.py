from django import forms
from .models import Budget, Transaction

# ফিক্সড ২৯টি ক্যাটাগরির কমন লিস্ট
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

class BudgetForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white'
        })
    )

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                'placeholder': 'বাজেটের পরিমাণ (টাকা)'
            }),
            'month': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                'placeholder': 'মাস (যেমন: 7)'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                'placeholder': 'বছর (যেমন: 2026)'
            }),
        }


class TransactionForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white'
        })
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'date', 'description', 'transaction_type']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                'placeholder': 'পরিমাণ (টাকা)'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                'placeholder': 'বিবরণ (ঐচ্ছিক)'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-white'
            }),
        }