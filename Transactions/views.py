
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ReceivingForm ,Receiving,DispatchForm,ReceivingReturnForm
from .models import Dispatch,ReceivingReturn,Receiving
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse


def add_receiving(request):
    if request.method == 'POST':
        form = ReceivingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('receiving_list')  # استبدل 'success_url' بالمسار الصحيح بعد الإضافة
    else:
        form = ReceivingForm()
    return render(request, 'transactions/add_receiving.html', {'form': form})

    # views.py


def receiving_list(request):
    # جلب جميع سجلات الاستلام
    receivings = Receiving.objects.all()
    return render(request, 'Transactions/receiving_list.html', {'receivings': receivings})






def create_dispatch(request):
    if request.method == 'POST':
        form = DispatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dispatch_list')  # أو أي وجهة أخرى بعد النجاح
    else:
        form = DispatchForm()
    return render(request, 'Transactions/create_dispatch.html', {'form': form})





def dispatch_list(request):
    # جلب جميع سجلات الاستلام
    dispatchs = Dispatch.objects.all()
    return render(request, 'Transactions/dispatch_list.html', {'dispatchs': dispatchs})















# def receiving_return_create(request):
#     if request.method == 'POST':
#         form = ReceivingReturnForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('receiving_return_create')  # استبدل هذا برابط النجاح المناسب
#     else:
#         form = ReceivingReturnForm()
#     return render(request, 'Transactions/receiving_return_form.html', {'form': form})

# def get_receiving_details(request, id):
#     receiving = get_object_or_404(Receiving, id=id)
#     print(f"Request for receiving details with ID: {id}")
  
#     data = {
#         'receiving_date': receiving.receiving_date,  # تحويل التاريخ إلى صيغة قابلة للإرسال كـ JSON
#         'warehouse': receiving.warehouse.name,  # تأكد من استخدام الحقل المناسب
#         'supplier': receiving.supplier.full_name,  # تأكد من استخدام الحقل المناسب
#         'station': receiving.station.station_name,  # تأكد من استخدام الحقل المناسب
#         'item':  receiving.item.name,
    
#     }
#     return JsonResponse(data)



def receiving_return_create(request):
    if request.method == 'POST':
        form = ReceivingReturnForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الإرجاع بنجاح!")
            return redirect('receiving_return_create')  # استبدل هذا برابط النجاح المناسب
        else:
            messages.error(request, "هناك خطأ في البيانات المدخلة. يرجى التحقق مرة أخرى.")
    else:
        form = ReceivingReturnForm()
    return render(request, 'Transactions/receiving_return_form.html', {'form': form})

def get_receiving_details(request, id):
    try:
        receiving = get_object_or_404(Receiving, id=id)
        print(f"Request for receiving details with ID: {id}")
      
        data = {
            'receiving_date': receiving.receiving_date.strftime('%Y-%m-%d'),  # تحويل التاريخ إلى صيغة قابلة للإرسال كـ JSON
            'warehouse': receiving.warehouse.name,
            'supplier': receiving.supplier.full_name,
            'station': receiving.station.station_name,
            'item': receiving.item.name,
        }
        return JsonResponse(data)
    except Exception as e:
        print(f"Error fetching receiving details: {e}")
        return JsonResponse({'error': 'حدث خطأ أثناء استرداد تفاصيل الاستلام.'}, status=500)