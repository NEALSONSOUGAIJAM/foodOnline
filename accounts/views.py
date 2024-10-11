from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from . models import User,UserProfile
from django.contrib import messages,auth
from vendor.models import Vendor
from vendor.forms import VendorForm
from .utils import dectectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied


# Restrict the vendor from accessing the customer page

def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied



#Restrict the customer from accessing the vendor page



def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied
        
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)#form is ready save not yet and it will assign to the user whatever data inside the form
            # user.set_password(password)
            # user.role = User.CUSTOMER# inside user model customer///assign some other field save to th data
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()        
           

    else:    
      form = UserForm()
    context = {
        'form':form
    }
    return render(request,'accounts/registerUser.html',context)

def registerVender(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method== 'POST':
        form =UserForm()
        v_form= VendorForm()
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

        

    else:
        form =UserForm()
        v_form= VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request,'accounts/registerVender.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')# when personis login required  ///before u go to dashboard
def myAccount(request):
    user= request.user# the person who is login
    redirectUrl= dectectUser(user)
    return redirect (redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def custdashboard(request):
    return render(request,"accounts/custDashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def vendorDashboard(request):
    return render(request,"accounts/vendorDashboard.html")