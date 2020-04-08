import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from addresses.models import Address
from billing.models import BillingProfile 

from cart.models import Cart 

from eth.utils import unique_order_id_generator
# from django.contrib.auth.models import User

from django.conf import settings
User = settings.AUTH_USER_MODEL



ORDER_STATUS_CHOICES = (
	('created','Created'),
	('paid','Paid'),
	('shipped','Shipped'),
	('refunded','Refunded'),
)


class OrderManager(models.Manager):
	def new_or_get(self, billing_profile, cart_obj):
		created=False
		qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj,active=True, status= 'created')
		if qs.count() == 1:
			obj = qs.first()
		else:
			obj = self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
			created=True
		return obj , created

# class OrderManager(models.Manager):

# 	def get_or_create(self, request):
# 		cart_id	= request.session.get("cart_id", None)
# 		#qs = Cart.objects.filter(id=cart_id)
# 		qs = self.get_queryset().filter(id=cart_id)
# 		if qs.count() == 1:
# 			new_obj = False
# 			print('Cart ID exists ')
# 			#print(cart_id)
# 			cart_obj = qs.first()
# 			if request.user.is_authenticated and cart_obj.user is None:
# 				print(cart_obj.user)
# 				cart_obj.user = request.user 
# 				cart_obj.save()
# 		else:
# 			cart_obj = Cart.objects.new(user=request.user)
# 			new_obj = True
# 			request.session['cart_id'] = cart_obj.id

# 		return cart_obj, new_obj



#Unique #Random
	#AB31DE3
class Order(models.Model):
	user			= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
	order_id		= models.CharField(max_length=120, blank=True)
	billing_address	= models.ForeignKey(Address, related_name="billing_address", null=True, blank=True, on_delete=models.CASCADE) 
	shipping_address= models.ForeignKey(Address,related_name="shipping_address", null=True, blank=True, on_delete=models.CASCADE)
	cart 			= models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE)
	status 			= models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	shipping_total	= models.DecimalField(default=20.00, max_digits=100, decimal_places=2)	
	total 			= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	active			= models.BooleanField(default=True)

	# objects = OrderManager()


	def __str__(self):
		return "ORDER-NO - {order}".format(order = self.order_id,)

		# return "order-NO -{order} ,      {user}".format(order = self.order_id,user = self.billing_profile or "",)

		# (self.order_id+ "\n" +self.user)

	objects = OrderManager()

	def update_total(self):
		cart_total = self.cart.total 
		shipping_total = self.shipping_total
		new_total = math.fsum([cart_total, shipping_total])
		formatted_total = format(new_total, '.2f')
		self.total = formatted_total
		self.save()
		return formatted_total


	def check_done(self):
		billing_profile 	= self.billing_profile
		shipping_address 	= self.shipping_address
		billing_address 	= self.billing_address
		total 				= self.total	

		if billing_profile and shipping_address and billing_address and total > 0:
			return True
		return False

	def mark_paid(self):
		if self.check_done():
			self.status = "paid"
			self.save()
		return self.status	

def pre_save_create_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)
	qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		cart_obj = instance
		cart_total = cart_obj.total 
		cart_id = cart_obj.id 
		qs = Order.objects.filter(cart_id=cart_id)
		if qs.count() == 1:
			order_obj = qs.first()
			order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
	print("hello this is before created portion..")
	if created:
		print("this is updating everything now...")
		instance.update_total()
		 
post_save.connect(post_save_order, sender=Order)
