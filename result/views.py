from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

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
    if not request.user.is_authenticated:
        return redirect('admin-login')
    return render(request,'admin_dashboard.html')

@login_required
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


def admin_logout(request):
    logout(request)
    return redirect('admin-login')

from django.shortcuts import get_object_or_404
@login_required
def manage_classes(request):
    classes = Class.objects.all()
    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_obj = get_object_or_404(Class,id=class_id)
            class_obj.delete()
            messages.success(request,"Class deleted successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong:{str(e)}")
    else:
        messages.error(request,f"Something went wrong:{str(e)}")

    return render(request,'manage_classes.html',locals())