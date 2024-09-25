
# Create your views here.

from django.shortcuts import render, redirect
from .models import Warehouse, Item 
from .forms import WarehouseForm 
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')

def warehouses_view(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'enventorys/warehouses/warehouses.html', {'warehouses': warehouses})

def items_view(request):
    items = Item.objects.all()
    return render(request, 'enventorys/items/items.html', {'items': items})



def add_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # استبدل 'success_url' بالمسار الذي تريد التوجيه إليه بعد الحفظ
    else:
        form = WarehouseForm()
    
    context = {
        'form': form
    }
    return render(request, 'enventorys/warehouses/warehouses.html', context)