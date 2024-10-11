from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from . models import User,UserProfile
from django.contrib import messages
from vendor.models import Vendor


# Create your views here.

        
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
    if request.method== 'POST':
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