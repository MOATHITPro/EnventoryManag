from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'password1', 'password2', 'user_type']
        labels = {
            'full_name': 'الاسم الكامل',
            'username': 'اسم المستخدم',
            'password1': 'كلمة المرور',
            'password2': 'تأكيد كلمة المرور',
            'user_type': 'نوع المستخدم',
        }