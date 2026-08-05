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
    
    # মাসিক পিডিএফ রিপোর্ট ডাউনলোডের পাথ
    path('download-pdf/', views.download_monthly_pdf, name='download_pdf'),
    
    # নতুন অ্যাকাউন্ট তৈরির (Signup) পাথ
    path('signup/', views.signup_view, name='signup'),
    
    # লগআউট (Logout) পাথ
    path('logout/', views.logout_view, name='logout'),

    # --- FinAI Chatbot & API Paths ---
    path('finai/', views.finai_chat_view, name='finai_chat'),
    path('api/finai-process/', views.finai_process_api, name='finai_process_api'),
]