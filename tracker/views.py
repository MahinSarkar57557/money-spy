import calendar
from datetime import date, datetime
from decimal import Decimal
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BudgetForm
from .models import Budget, Category, Transaction


# নতুন ব্যবহারকারী রেজিস্টার করার ভিউ
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


@login_required(login_url='login')
def dashboard_view(request):
  today = timezone.now().date()
  current_month = int(request.GET.get('month', today.month))
  current_year = int(request.GET.get('year', today.year))

  month_names = [
      '',
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
  ]
  month_name = month_names[current_month]

  transactions = Transaction.objects.filter(
      user=request.user, date__year=current_year, date__month=current_month
  )

  total_income = sum(
      t.amount for t in transactions if t.transaction_type == 'income'
  )
  total_expense = sum(
      t.amount for t in transactions if t.transaction_type == 'expense'
  )
  balance = total_income - total_expense

  all_categories = Category.objects.all()

  active_categories = []
  for cat in all_categories:
    cat_total = sum(
        t.amount
        for t in transactions.filter(
            category=cat, transaction_type='expense'
        )
    )
    if cat_total > 0:
      percentage = (
          round((cat_total / total_expense) * 100, 1)
          if total_expense > 0
          else 0
      )
      active_categories.append({
          'id': cat.id,
          'name': cat.name,
          'icon': cat.icon,
          'percentage': percentage,
          'total': cat_total,
      })

  processed_categories = []
  conic_gradient_stops = []
  current_deg = 0

  colors = [
      '#10b981',
      '#f59e0b',
      '#ef4444',
      '#3b82f6',
      '#8b5cf6',
      '#ec4899',
      '#14b8a6',
      '#f97316',
  ]

  for index, cat in enumerate(active_categories):
    deg_span = (cat['percentage'] / 100) * 360 if total_expense > 0 else 0
    start_deg = current_deg
    end_deg = current_deg + deg_span

    actual_mid_deg = start_deg + (deg_span / 2)
    mid_angle_rad = math.radians(actual_mid_deg - 90)

    radius = 56
    top_pos = 50 + radius * math.sin(mid_angle_rad)
    left_pos = 50 + radius * math.cos(mid_angle_rad)

    cat_color = colors[index % len(colors)]
    conic_gradient_stops.append(f'{cat_color} {start_deg}deg {end_deg}deg')
    current_deg = end_deg

    processed_categories.append({
        'id': cat['id'],
        'name': cat['name'],
        'icon': cat['icon'],
        'percentage': cat['percentage'],
        'total': cat['total'],
        'color': cat_color,
        'top': round(top_pos, 2),
        'left': round(left_pos, 2),
        'angle': round(actual_mid_deg, 1),
    })

  gradient_css = (
      ', '.join(conic_gradient_stops)
      if conic_gradient_stops
      else '#e5e7eb 0deg 360deg'
  )

  context = {
      'current_month': current_month,
      'current_year': current_year,
      'month_name': month_name,
      'total_income': total_income,
      'total_expense': total_expense,
      'balance': balance,
      'categories': processed_categories,
      'all_categories': all_categories,
      'gradient_css': gradient_css,
      'today': today,
  }

  return render(request, 'tracker/dashboard.html', context)


@login_required(login_url='login')
def calendar_view(request):
  today = timezone.localdate()
  current_month = int(request.GET.get('month', today.month))
  current_year = int(request.GET.get('year', today.year))

  transactions = Transaction.objects.filter(
      user=request.user, date__year=current_year, date__month=current_month
  )

  first_weekday, num_days = calendar.monthrange(current_year, current_month)

  daily_expenses = {}
  for t in transactions:
    if t.transaction_type == 'expense':
      day_num = t.date.day
      daily_expenses[day_num] = daily_expenses.get(day_num, 0) + t.amount

  calendar_days = []

  for _ in range(first_weekday):
    calendar_days.append({'day': ''})

  for day in range(1, num_days + 1):
    d_date = date(current_year, current_month, day)
    expense = daily_expenses.get(day, 0)
    calendar_days.append({
        'day': day,
        'date': d_date,
        'expense': expense if expense > 0 else None,
        'is_today': d_date == today,
    })

  last_7_days = []
  max_expense = 1
  temp_expenses = []

  for i in range(6, -1, -1):
    d = today - timezone.timedelta(days=i)
    day_name_str = d.strftime('%a')
    day_expense = (
        Transaction.objects.filter(
            user=request.user, date=d, transaction_type='expense'
        ).aggregate(total=models.Sum('amount'))['total']
        or 0
    )

    temp_expenses.append({'day_name': day_name_str, 'expense': day_expense})
    if day_expense > max_expense:
      max_expense = day_expense

  for item in temp_expenses:
    height_pct = int((float(item['expense']) / float(max_expense)) * 100)
    if height_pct < 8 and item['expense'] > 0:
      height_pct = 8
    elif item['expense'] == 0:
      height_pct = 4

    last_7_days.append({
        'day_name': item['day_name'],
        'expense': item['expense'],
        'height_percentage': height_pct,
    })

  context = {
      'calendar_days': calendar_days,
      'current_month': current_month,
      'current_year': current_year,
      'month_name': calendar.month_name[current_month],
      'last_7_days': last_7_days,
  }
  return render(request, 'tracker/calendar.html', context)


@login_required(login_url='login')
def add_transaction(request):
  if request.method == 'POST':
    transaction_type = request.POST.get('transaction_type')
    category_id = request.POST.get('category')
    amount = request.POST.get('amount')
    date_str = request.POST.get('date')
    description = request.POST.get('description', '')

    if amount and category_id:
      category = get_object_or_404(Category, id=category_id)
      Transaction.objects.create(
          user=request.user,
          transaction_type=transaction_type,
          category=category,
          amount=Decimal(amount),
          date=(
              datetime.strptime(date_str, '%Y-%m-%d').date()
              if date_str
              else timezone.now().date()
          ),
          description=description,
      )
  return redirect('dashboard')


@login_required(login_url='login')
def day_detail(request, year, month, day):
  target_date = date(year, month, day)
  transactions = Transaction.objects.filter(user=request.user, date=target_date)
  context = {
      'target_date': target_date,
      'transactions': transactions,
  }
  return render(request, 'tracker/day_detail.html', context)


@login_required(login_url='login')
def clear_today_transactions(request):
  today = timezone.localdate()
  Transaction.objects.filter(user=request.user, date=today).delete()
  return redirect('dashboard')


@login_required(login_url='login')
def budget_view(request):
  today = date.today()
  current_month = int(request.GET.get('month', today.month))
  current_year = int(request.GET.get('year', today.year))

  budgets = Budget.objects.filter(
      user=request.user, month=current_month, year=current_year
  )

  budget_data = []
  total_budget_amount = Decimal('0')
  total_spent_amount = Decimal('0')

  for b in budgets:
    spent = (
        Transaction.objects.filter(
            user=request.user,
            category=b.category,
            transaction_type='expense',
            date__year=current_year,
            date__month=current_month,
        ).aggregate(total=Sum('amount'))['total']
        or 0
    )

    spent_decimal = Decimal(str(spent))
    budget_amount_decimal = Decimal(str(b.amount))

    remaining = budget_amount_decimal - spent_decimal

    percentage = (
        int((spent_decimal / budget_amount_decimal) * 100)
        if budget_amount_decimal > 0
        else 0
    )

    rem_percentage = (
        float((remaining / budget_amount_decimal) * 100)
        if budget_amount_decimal > 0
        else 0
    )

    total_budget_amount += budget_amount_decimal
    total_spent_amount += spent_decimal

    budget_data.append({
        'budget': b,
        'spent': spent_decimal,
        'remaining': remaining,
        'percentage': min(percentage, 100),
        'rem_percentage': rem_percentage,
        'is_exceeded': spent_decimal > budget_amount_decimal,
    })

  if request.method == 'POST':
    form = BudgetForm(request.POST)
    if form.is_valid():
      budget_item = form.save(commit=False)
      budget_item.user = request.user
      Budget.objects.update_or_create(
          user=request.user,
          category=budget_item.category,
          month=budget_item.month,
          year=budget_item.year,
          defaults={'amount': budget_item.amount},
      )
      return redirect(f'/budget/?month={current_month}&year={current_year}')
  else:
    form = BudgetForm(initial={'month': current_month, 'year': current_year})

  all_categories = Category.objects.all()

  context = {
      'budget_data': budget_data,
      'form': form,
      'current_month': current_month,
      'current_year': current_year,
      'total_budget_amount': total_budget_amount,
      'total_spent_amount': total_spent_amount,
      'month_name': calendar.month_name[current_month],
      'all_categories': all_categories,
  }
  return render(request, 'tracker/budget.html', context)


@login_required(login_url='login')
def edit_budget(request, pk):
  budget_item = get_object_or_404(Budget, pk=pk, user=request.user)

  if request.method == 'POST':
    form = BudgetForm(request.POST, instance=budget_item)
    if form.is_valid():
      form.save()
      return redirect(
          f'/budget/?month={budget_item.month}&year={budget_item.year}'
      )
  else:
    form = BudgetForm(instance=budget_item)

  context = {
      'form': form,
      'budget_item': budget_item,
  }
  return render(request, 'tracker/edit_budget.html', context)


@login_required(login_url='login')
def settings_view(request):
  return render(request, 'tracker/settings.html')