from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # লগইন পেজ পাথ (name='login' থাকা বাধ্যতামূলক)
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    
    # লগআউট পেজ পাথ
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # আপনার অ্যাপের ইউআরএল
    path('', include('tracker.urls')),
]