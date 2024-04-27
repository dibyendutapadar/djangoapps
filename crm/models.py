from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    organizationName = models.CharField(max_length=255)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_created_by')
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_updated_by')
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organizationName

class Contact(models.Model):
    contactName = models.CharField(max_length=255)
    birthday = models.DateField()
    jobTitle = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_created_by')
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_updated_by')
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contactName

# For emails, phone numbers, and addresses, we create separate models 
# and link them to Contacts and Organizations with a ForeignKey.

class Email(models.Model):
    email_id = models.EmailField()
    type = models.CharField(max_length=50, choices=(('Work', 'Work'), ('Personal', 'Personal'), ('Other', 'Other')))
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_emails', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_emails', null=True, blank=True)

class PhoneNumber(models.Model):
    number = models.CharField(max_length=20)
    type = models.CharField(max_length=50, choices=(('Work', 'Work'), ('Mobile', 'Mobile'), ('Home', 'Home'), ('Fax', 'Fax'), ('Other', 'Other')))
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_phones', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_phones', null=True, blank=True)

class Address(models.Model):
    address = models.TextField()
    type = models.CharField(max_length=50, choices=(('Work', 'Work'), ('Billing', 'Billing'), ('Shipping', 'Shipping'), ('Home', 'Home'), ('Other', 'Other')))
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_addresses', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_addresses', null=True, blank=True)

class ContactStatus(models.Model):
    STATUS_CHOICES = (
        ('Contact', 'Contact'),
        ('Lead', 'Lead'),
        ('Customer', 'Customer'),
    )
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Contact')

    def __str__(self):
        return f"{self.contact.contactName} - {self.status}"    
