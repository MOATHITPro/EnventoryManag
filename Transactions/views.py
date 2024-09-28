
from django.shortcuts import render, redirect
from .forms import ReceivingForm ,Receiving,DispatchForm
    # views.py
from .models import Dispatch

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

