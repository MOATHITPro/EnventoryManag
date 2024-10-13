
# # Create your views here.
# from django.shortcuts import render

# # Create your views here.

# def signin(request):
#     return render (request,'users/signin.html')

# def signup(request):
#     return render (request,'users/signup.html')





from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .decorators import manager_required, operator_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_redirect')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
@manager_required
def manager_dashboard(request):
    return render(request, 'accounts/manager_dashboard.html')

@login_required
@operator_required
def operator_dashboard(request):
    return render(request, 'accounts/operator_dashboard.html')

@login_required
def login_redirect(request):
    if request.user.user_type == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('operator_dashboard')
