from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

# from django.contrib.auth.models import User

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

import stripe
stripe.api_key = "sk_test_ZoaMYzUyKgz9NDUJXoSzZ76V00vPUY2xTB"
#stripe.api_key = 'sk_test_ZoaMYzUyKgz9NDUJXoSzZ76V00vPUY2xTB'

intent = stripe.PaymentIntent.create(
  amount=1099,
  currency='inr',
)

# abc@teamcfe.com		--> 1000000 billing profiles 
# user abc@teamcfe.com 	--> 1 billing profile

class BillingProfileManager(models.Manager):

	def new_or_get(self, request):
		user = request.user 
		guest_email_id = request.session.get('guest_email_id')
		obj= None
		created=False
		if user.is_authenticated:
			#'Logged in user checkout; remember payment stuff'
			obj, created = self.model.objects.get_or_create(user=user, email=user.email)
		elif guest_email_id is not None:
			#'guest user checkout; auto reloads payment stuff'
			guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
			obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
		else:
			pass
		return obj, created 

class BillingProfile(models.Model):
	user 			= models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	email			= models.EmailField()
	active			= models.BooleanField(default=True)
	update			= models.DateTimeField(auto_now=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	customer_id 	= models.CharField(max_length=120, null=True, blank=True)
	#customer_id in Stripe or Braintree

	objects = BillingProfileManager()

	def __str__(self):
		return "Name:--> {user} ,  BillingProfile Email:--> {email}".format(user = self.user ,email= self.email)


# def billing_profile_created_reciever(sender, instance, created, *args, **kwargs):
# 	if not instance.customer_id and instance.email:
# 		print("ACTUAL API request send to stripe / braintree")
# 		customer = stripe.Customer.create(email=instance.email)
# 		print(customer)
# 		instance.customer_id= customer.id
# 		# instance.save()
	

def billing_profile_created_reciever(sender, instance, *args, **kwargs):
	if not instance.customer_id and instance.email:
		print("ACTUAL API request send to stripe / braintree")
		customer = stripe.Customer.create(email=instance.email)
		print(customer)
		instance.customer_id = customer.id
		# instance.save()
	else:
		pass

pre_save.connect(billing_profile_created_reciever, sender=BillingProfile)

	# if created:
	# 	print("ACTUAL API request send to stripe / braintree")
	# 	instance.customer_id = newID
	# 	instance.save()

def user_created_reciever(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_reciever, sender=User)		



class CardManager(models.Manager):
	def add_new(self, billing_profile, stripe_card_response):
		if str(stripe_card_response.object) == "card":
			new_card = self.model(
					billing_profile=billing_profile,
					stripe_id=stripe_card_response.id,
					brand=stripe_card_response.brand,
					country = stripe_card_response.country,
					exp_month = stripe_card_response.exp_month,
					exp_year = stripe_card_response.exp_year,
					last4 = stripe_card_response.last4
				)
			new_card.save()
			return new_card
		return None



class Card(models.Model):
	billing_profile 			= models.ForeignKey(BillingProfile, on_delete=models.CASCADE) 
	stripe_id					= models.CharField(max_length=120)
	brand 						= models.CharField(max_length=120, null=True, blank=True)
	country 					= models.CharField(max_length=120, null=True, blank=True)
	exp_month 					= models.IntegerField(null=True, blank= True)
	exp_year 					= models.IntegerField(null=True, blank= True)
	last4 						= models.CharField(max_length=4, null=True, blank= True)


	objects = CardManager()

	def __str__(self):
		return "{} {}".format(self.brand,self.last4)

