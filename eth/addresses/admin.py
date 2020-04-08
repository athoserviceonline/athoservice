from django.contrib import admin

from .models import Address

class AddressAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'billing_profile']
	class Meta:
		model = Address

admin.site.register(Address, AddressAdmin)


# admin.site.register(Address)