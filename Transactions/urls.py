

from django.urls import path
from .views import add_receiving,receiving_list,create_dispatch,dispatch_list,get_receiving_details,receiving_return_create

urlpatterns = [
    path('add_receiving/', add_receiving, name='add_receiving'),
    path('receivings/', receiving_list, name='receiving_list'),
    path('create_dispatch/', create_dispatch, name='create_dispatch'),
    path('dispatchs/', dispatch_list, name='dispatch_list'),
    path('receiving-return/create/', receiving_return_create, name='receiving_return_create'),  # رابط لإنشاء عملية إرجاع الوارد
    path('receiving/<int:id>/details/', get_receiving_details, name='get_receiving_details'),  # رابط لجلب تفاصيل عملية الوارد
]
