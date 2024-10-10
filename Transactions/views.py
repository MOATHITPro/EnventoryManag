
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ReceivingForm ,Receiving,DispatchForm,ReceivingReturnForm,DispatchReturnForm,DamageOperationForm,TransferOperationForm, TransferItemForm
from .models import Dispatch,ReceivingReturn,Receiving,DispatchReturn,DamageOperation,TransferOperation, TransferItem
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

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







        
def dispatch_return_create(request):
    if request.method == 'POST':
        form = DispatchReturnForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الإرجاع بنجاح!")
            return redirect('dispatch_return_create')  # استبدل هذا برابط النجاح المناسب
        else:
            messages.error(request, "هناك خطأ في البيانات المدخلة. يرجى التحقق مرة أخرى.")
    else:
        form = DispatchReturnForm()
    return render(request, 'Transactions/dispatch_return_form.html', {'form': form})

def get_dispatch_details(request, id):
    try:
        dispatch = get_object_or_404(Dispatch, id=id)
        print(f"Request for dispatch details with ID: {id}")
      
        data = {
            'dispatch_date': dispatch.dispatch_date.strftime('%Y-%m-%d'),  # تحويل التاريخ إلى صيغة قابلة للإرسال كـ JSON
            'warehouse': dispatch.warehouse.name,
            'beneficiary': dispatch.beneficiary.full_name,
            'item': dispatch.item.name,
        }
        return JsonResponse(data)
    except Exception as e:
        print(f"Error fetching dispatch details: {e}")
        return JsonResponse({'error': 'حدث خطأ أثناء استرداد تفاصيل الاستلام.'}, status=500)








class DamageOperationCreateView(CreateView):
    model = DamageOperation
    form_class = DamageOperationForm
    template_name = 'Transactions/damage_operation_form.html'
    success_url = reverse_lazy('create-damage-operation')

    def form_valid(self, form):
        # تنفيذ التحقق الخاص بك أو تخصيص البيانات هنا إذا لزم الأمر
        return super().form_valid(form)
        








def transfer_create_view(request):
    if request.method == 'POST':
        operation_form = TransferOperationForm(request.POST, request.FILES)
        item_form = TransferItemForm(request.POST)
        
        if operation_form.is_valid() and item_form.is_valid():
            transfer_operation = operation_form.save()
            transfer_item = item_form.save(commit=False)
            transfer_item.transfer_operation = transfer_operation
            transfer_item.save()
            return redirect('transfer_create')  # Redirect to a success page after saving
    else:
        operation_form = TransferOperationForm()
        item_form = TransferItemForm()

    context = {
        'operation_form': operation_form,
        'item_form': item_form,
    }
    return render(request, 'Transactions/transfer_form.html', context)

def transfer_success_view(request):
    return render(request, 'Transactions/transfer_success.html')
