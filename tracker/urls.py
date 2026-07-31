from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('budget/', views.budget_view, name='budget'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('day/<int:year>/<int:month>/<int:day>/', views.day_detail, name='day_detail'),
    path('settings/', views.settings_view, name='settings'),
    path('budget/edit/<int:pk>/', views.edit_budget, name='edit_budget'),
    path('clear-today/', views.clear_today_transactions, name='clear_today_transactions'),
]