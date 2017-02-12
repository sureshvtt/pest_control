from django.contrib import admin

from customer.models import Customer, EnquiryService, Enquiry, Contract

admin.site.register(Customer)
admin.site.register(EnquiryService)
admin.site.register(Enquiry)
admin.site.register(Contract)