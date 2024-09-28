
# Create your views here.

from django.shortcuts import render, redirect
from .models import Warehouse, Item,StockItem ,Station,Supplier,Beneficiary
from .forms import WarehouseForm ,ItemForm,StockItemForm,StationForm,SupplierForm,BeneficiaryForm
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
            form.save()  # حفظ العنصر في قاعدة البيانات
            return redirect('warehouses')  # إعادة توجيه إلى قائمة العناصر
    else:
        form = WarehouseForm()

    return render(request, 'enventorys/warehouses/warehouses.html', {'form': form})
   
def additem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()  # حفظ العنصر في قاعدة البيانات
            return redirect('items')  # إعادة توجيه إلى قائمة العناصر
    else:
        form = ItemForm()

    return render(request, 'enventorys/items/items.html', {'form': form})








def stockitems_view(request):
    add_stock_items = StockItem.objects.all()
    return render(request, 'enventorys/items/add_stock_items.html', {'add_stock_items': add_stock_items})

def add_stock_item_view(request):
    items = Item.objects.all()
    warehouses = Warehouse.objects.all()

    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_stock_item')  # تأكد من الاسم هنا
    else:
        form = StockItemForm()

    return render(request, 'enventorys/items/add_stock_items.html', {
        'form': form,
        'items': items,
        'warehouses': warehouses,
        'add_stock_items': StockItem.objects.all()  # إعادة البيانات هنا
    })











def station_view(request):
    stations = Station.objects.all()
    return render(request, 'enventorys/stations/stations.html', {'stations': stations})

def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()  # حفظ العنصر في قاعدة البيانات
            return redirect('stations')  # إعادة توجيه إلى قائمة العناصر
    else:
        form = StationForm()

    return render(request, 'enventorys/stations/stations.html', {'form': form})
   

def supplier_view(request):
    suppliers = Supplier.objects.all()
    return render(request, 'enventorys/suppliers/suppliers.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()  # حفظ العنصر في قاعدة البيانات
            return redirect('suppliers')  # إعادة توجيه إلى قائمة العناصر
    else:
        form = SupplierForm()

    return render(request, 'enventorys/suppliers/suppliers.html', {'form': form})
     


 
def beneficiary_view(request):
    beneficiarys = Beneficiary.objects.all()
    return render(request, 'enventorys/beneficiarys/beneficiarys.html', {'beneficiarys': beneficiarys})

def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            form.save()  # حفظ العنصر في قاعدة البيانات
            return redirect('beneficiarys')  # إعادة توجيه إلى قائمة العناصر
    else:
        form = BeneficiaryForm()

    return render(request, 'enventorys/beneficiarys/beneficiarys.html', {'form': form})
         