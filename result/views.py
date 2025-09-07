from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')
    
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    error = None
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid"


    return render(request,'admin_login.html',locals()) 

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')


def create_class(request):

    if request.method == 'POST':
        try:
            class_name = request.POST.get('classname')
            class_numeric = request.POST.get('classnamenumeric')
            section = request.POST.get('section')
            Class.objects.create(class_name=class_name,class_numeric=class_numeric,section=section)
            message.success(request,"Class created successfully")
            redirect(create_class)


        except Exception as e:
            messages.error(request,f"Something went wrong:{str(e)}")

    
    return render(request,'create_class.html')