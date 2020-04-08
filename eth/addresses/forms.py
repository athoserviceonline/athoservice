from django import forms
from django.forms import ModelForm


from .models import Address

class AddressForm(ModelForm):
	
	class Meta:
			model = Address 		
			fields= [
			'address_line_1',
			'address_line_2',
			'city',
			'country',
			'states',
			'postal_code',
			]			



#fields= '__all__'
		

