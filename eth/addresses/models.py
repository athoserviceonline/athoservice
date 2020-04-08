from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
	('billing', 'Billing'),
	('shipping', 'Shipping'),
)


class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
	address_type	= models.CharField(max_length=120, choices= ADDRESS_TYPES)
	address_line_1	= models.CharField(max_length=120)
	address_line_2	= models.CharField(max_length=120, null=True, blank=True)
	city			= models.CharField(max_length=120)	
	country			= models.CharField(max_length=120, default='India')
	states			= models.CharField(max_length=120)
	postal_code		= models.CharField(max_length=120)
	
	def __str__(self):
		return "{line1}, {line2}, {city}, {state}, {postal}, {country}".format(
			line1 = self.address_line_1,
			line2 = self.address_line_2 or "",
			city = self.city,
			state = self.states,
			postal = self.postal_code,
			country = self.country,
			)

	def get_address(self):
		return "address1- {line1}, \naddress2- {line2}, \ncity- {city}, \nstate- {state}, pincode- {postal}, \ncountry- {country}".format(
			line1 = self.address_line_1,
			line2 = self.address_line_2 or "",
			city = self.city,
			state = self.states,
			postal = self.postal_code,
			country = self.country,
			)