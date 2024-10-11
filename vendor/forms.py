from django import forms
from .models import Vendor, OpeningHour



class VendorForm(forms.ModelForm):
   
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
