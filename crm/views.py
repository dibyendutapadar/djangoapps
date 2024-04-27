from django.shortcuts import render, redirect
import requests
from .models import Contact
from .forms import ContactForm
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def admin_home(request):
    return render(request, 'admin_home.html')

def admin_contact(request):
    contacts_list = Contact.objects.all().select_related('organization')  # Adjust the query as needed
    paginator = Paginator(contacts_list, 10)  # Show 10 contacts per page

    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    return render(request, 'admin_contact.html', {'contacts': contacts})

# views.py
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to contacts list page or elsewhere
            return redirect('admin_contact')
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})        
   




# --------------------------------------------
def custom_add_contact_view(request):
    # Retrieve the ModelAdmin instance for the Contact model
    contact_admin = admin.site._registry[Contact]
    
    # Initialize the ModelForm for adding a Contact. Use the same form as the admin.
    ModelForm = contact_admin.get_form(request)
    
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            # Mimic the save logic from the admin form
            new_contact = form.save()
            # Redirect after successful creation
            return HttpResponseRedirect(reverse('admin_contact'))
    else:
        form = ModelForm()

    # The context for rendering the template
    context = {
        'form': form,
        'adminform': form,  # admin templates expect an adminform context variable
        # Include other context variables required by your admin template
    }

    # Render the admin template or a custom template that extends the admin layout
    return render(request, 'admin/crm/contact/add', context)