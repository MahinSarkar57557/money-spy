from django import forms
from .models import Budget, Category

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50',
                'placeholder': 'বাজেটের পরিমাণ (টাকা)'
            }),
            'month': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50',
                'placeholder': 'মাস (যেমন: 7)'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-gray-50',
                'placeholder': 'বছর (যেমন: 2026)'
            }),
        }