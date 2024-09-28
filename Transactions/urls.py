

from django.urls import path
from .views import add_receiving,receiving_list,create_dispatch,dispatch_list

urlpatterns = [
    path('add_receiving/', add_receiving, name='add_receiving'),
    path('receivings/', receiving_list, name='receiving_list'),
    path('create_dispatch/', create_dispatch, name='create_dispatch'),
    path('dispatchs/', dispatch_list, name='dispatch_list'),

]
