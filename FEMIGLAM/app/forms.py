from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=True)
