from django import forms
from django.forms import inlineformset_factory
from .models import Contact, Email, PhoneNumber, Address

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contactName', 'birthday', 'jobTitle', 'designation', 'department', 'organization']

EmailFormSet = inlineformset_factory(Contact, Email, fields=('email_id', 'type'), extra=1, can_delete=True)
PhoneNumberFormSet = inlineformset_factory(Contact, PhoneNumber, fields=('number', 'type'), extra=1, can_delete=True)
AddressFormSet = inlineformset_factory(Contact, Address, fields=('address', 'type'), extra=1, can_delete=True)
