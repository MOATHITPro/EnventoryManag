

from django.urls import path
from .views import add_receiving,receiving_list,create_dispatch,dispatch_list,get_receiving_details,receiving_return_create,dispatch_return_create,get_dispatch_details,DamageOperationCreateView
from django.views.generic import TemplateView  # أضف هذا السطر لاستيراد TemplateView

urlpatterns = [
    path('add_receiving/', add_receiving, name='add_receiving'),
    path('receivings/', receiving_list, name='receiving_list'),
    path('create_dispatch/', create_dispatch, name='create_dispatch'),
    path('dispatchs/', dispatch_list, name='dispatch_list'),
    path('receiving-return/create/', receiving_return_create, name='receiving_return_create'),  # رابط لإنشاء عملية إرجاع الوارد
    path('receiving/<int:id>/details/', get_receiving_details, name='get_receiving_details'),  # رابط لجلب تفاصيل عملية الوارد

    path('dispatch-return/create/', dispatch_return_create, name='dispatch_return_create'),  # رابط لإنشاء عملية إرجاع الوارد
    path('dispatch/<int:id>/details/', get_dispatch_details, name='get_dispatch_details'),  # رابط لجلب تفاصيل عملية الوارد

    path('create-damage-operation/', DamageOperationCreateView.as_view(), name='create-damage-operation'),
]

