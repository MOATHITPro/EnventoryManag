
# Create your views here.
from django.shortcuts import render

# Create your views here.

def signin(request):
    return render (request,'users/signin.html')

def signup(request):
    return render (request,'users/signup.html')