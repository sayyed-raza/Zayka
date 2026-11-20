from django.urls import path
from. import views

from django.contrib.auth.views import LogoutView

urlpatterns =[
    path('register/user/', views.RegisterUserView.as_view(), name='register-user'),
    path('register/vendor/', views.register_vendor, name='register-vendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='dashboard'),
    path('customer/profile/', views.customer_profile, name='customer-dashboard'),
    path('vendor/profile/', views.vendor_profile, name='vendor-dashboard'),
]