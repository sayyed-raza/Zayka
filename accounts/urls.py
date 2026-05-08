from django.urls import path
from. import views

from django.contrib.auth.views import LogoutView

urlpatterns =[
    path('register/user/', views.RegisterUserView.as_view(), name='register-user'),
    path('register/vendor/', views.register_vendor, name='register-vendor'),
]