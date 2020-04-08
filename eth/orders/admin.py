from django.contrib import admin

from .models import Order

# from django.contrib.auth.models import User

# admin.site.register(Order)
# try:
# def case_name():
#     return ("%s, %s" % (billing_address.address_line_1, billing_address.address_line_2))
# case_name.short_description = 'Address'
# except NoneType:
# 	pass
# class PersonAdmin(admin.ModelAdmin):
#     list_display = (case_name,)



class OrderAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'billing_profile']
	class Meta:
		model = Order
	# if case_name:	
	# list_display = (case_name,)
	# else:
		# fields= [
		# 	'address_line_1',
		# 	'address_line_2',
		# 	'city',
		# 	'country',
		# 	'states',
		# 	'postal_code',
		# 	]
admin.site.register(Order, OrderAdmin)

