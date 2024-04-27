from django.contrib import admin

# Register your models here.
from .models import Contact, Organization, Email, PhoneNumber, Address, ContactStatus

class EmailInline(admin.TabularInline):
    model = Email
    extra = 1  # Number of empty extra forms

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class ContactAdmin(admin.ModelAdmin):
    inlines = [EmailInline, PhoneNumberInline, AddressInline]
    list_display = ('contactName', 'organization', 'createdBy', 'createdOn')
    search_fields = ('contactName', 'organization__organizationName')

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [EmailInline, PhoneNumberInline, AddressInline]
    list_display = ('organizationName', 'createdBy', 'createdOn')
    search_fields = ('organizationName',)

# Now, instead of the simple register function, use the admin.site.register() with the custom ModelAdmin
admin.site.register(Contact, ContactAdmin)
admin.site.register(Organization, OrganizationAdmin)

# You can keep the simple registration for Email, PhoneNumber, and Address if no customization is needed
admin.site.register(Email)
admin.site.register(PhoneNumber)
admin.site.register(Address)

admin.site.register(ContactStatus)