"""
URL configuration for Enventory_Manag project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .import home
from django.contrib.auth import views as auth_views

# urlpatterns = [

#     path('admin/', admin.site.urls),
#     path('',home.index,name='index'),
#     path('', include("Enventory.urls")),
#     path('accounts/', include ('Accounts.urls')),
#     path('transactions/', include('Transactions.urls')),  # تأكد من تضمين URLs التطبيق
#     path('reports/', include('Reports.urls')),  # تأكد من تضمين URLs التطبيق

# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # توجيه المستخدمين غير المسجلين الدخول إلى صفحة تسجيل الدخول
    path('', lambda request: redirect('login') if not request.user.is_authenticated else redirect('index'), name='home'),
    
    # الصفحة الرئيسية
    path('', home.index, name='index'),

    # تضمين التطبيقات الأخرى
    path('', include("Enventory.urls")),
    path('accounts/', include('Accounts.urls')),
    path('transactions/', include('Transactions.urls')),
    path('reports/', include('Reports.urls')),

    # صفحة تسجيل الدخول
    path('login/', auth_views.LoginView.as_view(), name='login'),

]






if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
