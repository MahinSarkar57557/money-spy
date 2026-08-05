import calendar
from datetime import date, datetime
from decimal import Decimal
import math
import io
import json
import os
from openai import OpenAI  # OpenAI লাইব্রেরি ইমপোর্ট করা হলো
from django.http import FileResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BudgetForm
from .models import Budget, Transaction, CATEGORY_CHOICES


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

    expense_categories = [
        {"name": "Tuition & Fees", "icon": "fas fa-graduation-cap"},
        {"name": "Books & Notes", "icon": "fas fa-book"},
        {"name": "Stationery", "icon": "fas fa-pen"},
        {"name": "Courses & Training", "icon": "fas fa-laptop-code"},
        {"name": "Mess / Hall Bill", "icon": "fas fa-utensils"},
        {"name": "Restaurants & Fast Food", "icon": "fas fa-hamburger"},
        {"name": "Tea & Snacks", "icon": "fas fa-coffee"},
        {"name": "Groceries", "icon": "fas fa-shopping-basket"},
        {"name": "Bus / Local Transport", "icon": "fas fa-bus"},
        {"name": "Rickshaw & CNG", "icon": "fas fa-shuttle-van"},
        {"name": "Bike Fuel / Maintenance", "icon": "fas fa-motorcycle"},
        {"name": "Tour & Travel", "icon": "fas fa-plane"},
        {"name": "Rent / Room Rent", "icon": "fas fa-home"},
        {"name": "Electricity & Gas", "icon": "fas fa-bolt"},
        {"name": "Internet & WiFi", "icon": "fas fa-wifi"},
        {"name": "Mobile Recharge", "icon": "fas fa-mobile-alt"},
        {"name": "bKash / Nagad", "icon": "fas fa-wallet"},
        {"name": "Clothing & Tailoring", "icon": "fas fa-tshirt"},
        {"name": "Personal Care", "icon": "fas fa-cut"},
        {"name": "Medicine & Health", "icon": "fas fa-medkit"},
        {"name": "Gym & Sports", "icon": "fas fa-dumbbell"},
        {"name": "Entertainment & Subscriptions", "icon": "fas fa-film"},
        {"name": "Gift", "icon": "fas fa-gift"},
        {"name": "Donation", "icon": "fas fa-hand-holding-heart"},
        {"name": "Debt Repayment", "icon": "fas fa-undo-alt"},
        {"name": "Tech & Gadgets", "icon": "fas fa-laptop"},
        {"name": "Savings & Investment", "icon": "fas fa-piggy-bank"},
        {"name": "Miscellaneous / Others", "icon": "fas fa-box"},
    ]

    income_categories = [
        {"name": "Job", "icon": "fas fa-briefcase"},
        {"name": "Business", "icon": "fas fa-store"},
        {"name": "Freelancing", "icon": "fas fa-laptop-code"},
        {"name": "Tuition", "icon": "fas fa-chalkboard-teacher"},
        {"name": "Gift", "icon": "fas fa-gift"},
        {"name": "Money Back", "icon": "fas fa-undo-alt"},
        {"name": "Pocket Money", "icon": "fas fa-hand-holding-usd"},
    ]

    active_categories = []
    for cat in expense_categories:
        cat_name = cat["name"]
        cat_total = sum(
            t.amount
            for t in transactions.filter(
                category=cat_name, transaction_type='expense'
            )
        )
        if cat_total > 0:
            percentage = (
                round((cat_total / total_expense) * 100, 1)
                if total_expense > 0
                else 0
            )
            active_categories.append({
                'name': cat_name,
                'percentage': percentage,
                'total': cat_total,
                'icon': cat["icon"],
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
            'name': cat['name'],
            'percentage': cat['percentage'],
            'total': cat['total'],
            'icon': cat['icon'],
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
        'expense_categories': expense_categories,
        'income_categories': income_categories,
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

    current_month_total = sum(
        t.amount for t in transactions if t.transaction_type == 'expense'
    )

    if current_month == 1:
        prev_month = 12
        prev_year = current_year - 1
    else:
        prev_month = current_month - 1
        prev_year = current_year

    prev_transactions = Transaction.objects.filter(
        user=request.user, date__year=prev_year, date__month=prev_month, transaction_type='expense'
    )
    prev_month_total = sum(t.amount for t in prev_transactions)

    mom_percentage = 0
    mom_is_increase = False

    if prev_month_total > 0:
        diff = current_month_total - prev_month_total
        mom_percentage = abs(float((diff / prev_month_total) * 100))
        mom_is_increase = diff > 0
    elif current_month_total > 0:
        mom_percentage = 100.0
        mom_is_increase = True

    context = {
        'calendar_days': calendar_days,
        'current_month': current_month,
        'current_year': current_year,
        'month_name': calendar.month_name[current_month],
        'last_7_days': last_7_days,
        'current_month_total': current_month_total,
        'prev_month_total': prev_month_total,
        'mom_percentage': mom_percentage,
        'mom_is_increase': mom_is_increase,
    }
    return render(request, 'tracker/calendar.html', context)


@login_required(login_url='login')
def add_transaction(request):
    if request.method == 'POST':
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        date_str = request.POST.get('date')
        description = request.POST.get('description', '')

        if amount and category:
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
    try:
        current_month = int(request.GET.get('month', today.month))
        current_year = int(request.GET.get('year', today.year))
    except ValueError:
        current_month = today.month
        current_year = today.year

    expense_categories = [
        {"name": "Tuition & Fees", "icon": "fas fa-graduation-cap"},
        {"name": "Books & Notes", "icon": "fas fa-book"},
        {"name": "Stationery", "icon": "fas fa-pen"},
        {"name": "Courses & Training", "icon": "fas fa-laptop-code"},
        {"name": "Mess / Hall Bill", "icon": "fas fa-utensils"},
        {"name": "Restaurants & Fast Food", "icon": "fas fa-hamburger"},
        {"name": "Tea & Snacks", "icon": "fas fa-coffee"},
        {"name": "Groceries", "icon": "fas fa-shopping-basket"},
        {"name": "Bus / Local Transport", "icon": "fas fa-bus"},
        {"name": "Rickshaw & CNG", "icon": "fas fa-shuttle-van"},
        {"name": "Bike Fuel / Maintenance", "icon": "fas fa-motorcycle"},
        {"name": "Tour & Travel", "icon": "fas fa-plane"},
        {"name": "Rent / Room Rent", "icon": "fas fa-home"},
        {"name": "Electricity & Gas", "icon": "fas fa-bolt"},
        {"name": "Internet & WiFi", "icon": "fas fa-wifi"},
        {"name": "Mobile Recharge", "icon": "fas fa-mobile-alt"},
        {"name": "bKash / Nagad", "icon": "fas fa-wallet"},
        {"name": "Clothing & Tailoring", "icon": "fas fa-tshirt"},
        {"name": "Personal Care", "icon": "fas fa-cut"},
        {"name": "Medicine & Health", "icon": "fas fa-medkit"},
        {"name": "Gym & Sports", "icon": "fas fa-dumbbell"},
        {"name": "Entertainment & Subscriptions", "icon": "fas fa-film"},
        {"name": "Gift", "icon": "fas fa-gift"},
        {"name": "Donation", "icon": "fas fa-hand-holding-heart"},
        {"name": "Debt Repayment", "icon": "fas fa-undo-alt"},
        {"name": "Tech & Gadgets", "icon": "fas fa-laptop"},
        {"name": "Savings & Investment", "icon": "fas fa-piggy-bank"},
        {"name": "Miscellaneous / Others", "icon": "fas fa-box"},
    ]

    icon_dict = {cat["name"]: cat["icon"] for cat in expense_categories}

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

        cat_icon = icon_dict.get(str(b.category), "fas fa-wallet")

        budget_data.append({
            'budget': b,
            'spent': spent_decimal,
            'remaining': remaining,
            'percentage': min(percentage, 100),
            'rem_percentage': rem_percentage,
            'is_exceeded': spent_decimal > budget_amount_decimal,
            'icon': cat_icon,
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

    all_categories = [cat[0] for cat in CATEGORY_CHOICES]

    context = {
        'budget_data': budget_data,
        'form': form,
        'current_month': current_month,
        'current_year': current_year,
        'total_budget_amount': total_budget_amount,
        'total_spent_amount': total_spent_amount,
        'month_name': calendar.month_name[current_month],
        'all_categories': all_categories,
        'expense_categories': expense_categories,
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
def download_monthly_pdf(request):
    today = timezone.localdate()
    current_month = int(request.GET.get('month', today.month))
    current_year = int(request.GET.get('year', today.year))

    transactions = Transaction.objects.filter(
        user=request.user, 
        date__year=current_year, 
        date__month=current_month
    ).order_by('date')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Money Spy - Expense & Income Report")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Month: {calendar.month_name[current_month]} {current_year}")
    p.drawString(50, height - 85, f"Generated for: {request.user.username}")

    y = height - 120
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Date")
    p.drawString(130, y, "Type")
    p.drawString(200, y, "Category")
    p.drawString(350, y, "Amount (BDT)")
    p.drawString(430, y, "Description")

    p.line(50, y - 5, 550, y - 5)
    y -= 20

    p.setFont("Helvetica", 9)
    total_inc = 0
    total_exp = 0

    for t in transactions:
        if y < 50:
            p.showPage()
            y = height - 50
        
        p.drawString(50, y, str(t.date))
        p.drawString(130, y, t.transaction_type.capitalize())
        p.drawString(200, y, str(t.category)[:25])
        p.drawString(350, y, f"৳{t.amount}")
        p.drawString(430, y, str(t.description)[:20] if t.description else "-")

        if t.transaction_type == 'income':
            total_inc += t.amount
        else:
            total_exp += t.amount

        y -= 18

    y -= 10
    p.line(50, y, 550, y)
    y -= 20
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, f"Total Income: ৳{total_inc}")
    p.drawString(200, y, f"Total Expense: ৳{total_exp}")
    p.drawString(380, y, f"Net Balance: ৳{total_inc - total_exp}")

    p.showPage()
    p.save()
    buffer.seek(0)
    
    filename = f"MoneySpy_Report_{current_month}_{current_year}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)


@login_required(login_url='login')
def settings_view(request):
    return render(request, 'tracker/settings.html')


@login_required(login_url='login')
def finai_chat_view(request):
    return render(request, 'tracker/finai.html')


@login_required(login_url='login')
def finai_process_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'status': 'error', 'reply': 'দয়া করে কিছু লিখে বা বলে পাঠান।'})

            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                return JsonResponse({'status': 'error', 'reply': 'সার্ভারে OpenAI এপিআই কি কনফিগার করা নেই।'})

            client = OpenAI(api_key=api_key)

            user_transactions = Transaction.objects.filter(user=request.user)
            total_inc = sum(t.amount for t in user_transactions if t.transaction_type == 'income')
            total_exp = sum(t.amount for t in user_transactions if t.transaction_type == 'expense')
            current_balance = total_inc - total_exp

            system_prompt = f"""
            You are 'FinAI', an expert personal financial advisor and transaction parser for a user in Bangladesh.
            
            User's Real-time Financial Data:
            - Total Income: ৳{total_inc}
            - Total Expense: ৳{total_exp}
            - Current Balance: ৳{current_balance}

            Your tasks:
            1. If the user message is about adding an expense or income (e.g., "50 taka transport expense", "500 taka job income", "বই বাবদ ২০ টাকা খরচ"), set:
               - "action": "transaction"
               - "transaction_type": "expense" or "income"
               - "amount": numeric value
               - "category": Must strictly match one of the valid categories below.
               Valid Expense Categories: Tuition & Fees, Books & Notes, Stationery, Courses & Training, Mess / Hall Bill, Restaurants & Fast Food, Tea & Snacks, Groceries, Bus / Local Transport, Rickshaw & CNG, Bike Fuel / Maintenance, Tour & Travel, Rent / Room Rent, Electricity & Gas, Internet & WiFi, Mobile Recharge, bKash / Nagad, Clothing & Tailoring, Personal Care, Medicine & Health, Gym & Sports, Entertainment & Subscriptions, Gift, Donation, Debt Repayment, Tech & Gadgets, Savings & Investment, Miscellaneous / Others
               Valid Income Categories: Job, Business, Freelancing, Tuition, Gift, Money Back, Pocket Money
            
            2. If the user message is a greeting (like "hi", "hlw", "hello"), general query, or financial advice question, set:
               - "action": "advice"
               - "reply": Provide a friendly greeting or practical financial response in Bengali.

            User Message: "{user_message}"

            Return ONLY a valid JSON object. 
            If action is "transaction", keys must be: "action", "transaction_type", "amount", "category".
            If action is "advice", keys must be: "action", "reply".
            Do not include markdown formatting like ```json ... ```.
            """

            # OpenAI মডেল দিয়ে কল করা
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )
            
            clean_text = response.choices[0].message.content.strip()
            ai_data = json.loads(clean_text)
            action = ai_data.get('action', 'advice')

            if action == 'transaction':
                amount = Decimal(str(ai_data.get('amount', 0)))
                trans_type = ai_data.get('transaction_type', 'expense')
                category = ai_data.get('category', 'Miscellaneous / Others')

                if amount > 0:
                    Transaction.objects.create(
                        user=request.user,
                        transaction_type=trans_type,
                        category=category,
                        amount=amount,
                        date=timezone.now().date(),
                        description=user_message
                    )
                    bot_reply = f"✅ সফলভাবে সেভ করা হয়েছে! ৳{amount} ({category} - {'আয়' if trans_type=='income' else 'খরচ'}) হিসেবে যোগ করা হয়েছে।"
                else:
                    bot_reply = "দয়া করে সঠিক টাকার পরিমাণ উল্লেখ করুন।"
            else:
                bot_reply = ai_data.get('reply', 'হ্যালো! আমি আপনার ফিন্যান্সিয়াল অ্যাসিস্ট্যান্ট। বলুন কীভাবে সাহায্য করতে পারি?')

            return JsonResponse({'status': 'success', 'reply': bot_reply})
        except Exception as e:
            return JsonResponse({'status': 'error', 'reply': f'ত্রুটি: {str(e)}'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')