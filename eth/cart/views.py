from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.models import Address

from addresses.forms import AddressForm

from billing.models import BillingProfile 

from shopping.models import Product 
from .models import Cart 

from orders.models import Order


def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)	
	products = [{
			"id": x.id,
			"url": x.get_absolute_url(),
			"name": x.name, 
			"price": x.price,
			} 
			for x in cart_obj.products.all()] 

	cart_data = {"products": products,"subtotal": cart_obj.subtotal, "total": cart_obj.total}
	return JsonResponse(cart_data)
	
	# cart_obj.products.all() # [<object>, <object>, <object>]
	# products_list = []
	# for x in cart_obj.products.all():
	# 	products_list.append({"name": x.name, "price": x.price})

def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)	
	return render(request, "cart/home.html",{'cart':cart_obj})
	
def cart_update(request):
	#print(request.POST)
	product_id = request.POST.get('product_id')

	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user, product is gone outside")
			return redirect("cart:home")

		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False
		else:
			cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
			added = True
		request.session['cart_items'] = cart_obj.products.count()
	#cart_obj.title = "add"
	#cart_obj.save()
	#cart_obj.products.remove(obj)
	#return redirect(product_obj.get_absolute_url())

		if request.is_ajax():
			print("Ajax request")
			json_data = {
				"added": added,
				"removed": not added, 
				"cartItemCount": cart_obj.products.count(),
			}
			return JsonResponse(json_data, status=200) #status_code=200 / 201 # HttpResponse
			# return JsonResponse({"message": "Error 400"}, status_code=400) # Django rest framework
	return redirect("cart:home")


def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)	
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")
	# else:
	# 	try:
	# 		order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
	# 	except Order.MultipleObjectsReturned:
	# 		pass

	# user = request.user
	# billing_profile = 	None
	login_form				= 	LoginForm()
	guest_form				= 	GuestForm()
	address_form			=	AddressForm()
	billing_address_id		=	request.session.get("billing_address_id", None)
	shipping_address_id		=	request.session.get("shipping_address_id", None)

	# billing_address_form	=	AddressForm()

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	# guest_email_id 	=	request.session.get('guest_email_id')
	
	# if user.is_authenticated:
	# 	# if user.email:
	# 	billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)
	# elif guest_email_id is not None:
	# 	guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
	# 	billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
	# else:
	# 	pass

	address_qs = None
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)	
		# shipping_address_qs		= address_qs.filter(address_type='shipping')
		# billing_address_qs 		= address_qs.filter(address_type='billing')

		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if billing_address_id or shipping_address_id:
			order_obj.save()


	if request.method == "POST":
		"check that order is done"
		is_done 	= order_obj.check_done()
		if is_done:
			order_obj.mark_paid() 
			request.session['cart_items'] = 0
			del request.session['cart_id']
			return redirect("cart:success")

#		del request.session['cart_id']

	'''

	update order_obj to done, "paid"
	del request.session['cart_id']
	redirect "success"

	'''



		# order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)	
		# if order_qs.count() == 1:
		# 	order_obj = order_qs.first()
		# else:
		# 	# old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
		# 	# if old_order_qs.exists():
		# 	# 	old_order_qs.update(active=False)
		# 	order_obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)


		# order_qs = Order.objects.filter(cart=cart_obj, active=True)
		# if order_qs.exists():
		# 	order_qs.update(active=False)
		# else:
		# 	order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

	context = {
		"object": order_obj,
		"billing_profile": billing_profile,
		"login_form": login_form,
		"guest_form": guest_form,
		"address_form": address_form,
		# "billing_address_form": billing_address_form,
		"address_qs": address_qs,
	}

	return render(request, "cart/checkout.html", context)


def checkout_done_view(request):
	return render(request, "cart/checkout-done.html", {})




















# def cart_create(user=None):
# 	cart_obj = Cart.objects.create(user=None)
# 	print('New Cart created')
# 	return cart_obj


# def cart_home(request):
# 	cart_obj = Cart.objects.new_or_get(request)	
	#request.session['cart_id'] = "12"
	#del request.session['cart_id']
	# cart_id	= request.session.get("cart_id", None)
	# # if cart_id is None:  # and isinstance(cart_id,int)
	# # 	cart_obj = cart_create()
	# # 	#print('create new cart')
	# # 	request.session['cart_id'] = cart_obj.id #set
	# # 	# pass
	# # 	print('new cart created')
	# # else:
	# qs = Cart.objects.filter(id=cart_id)
	# if qs.count() == 1:
	# 	print('Cart ID exists ')
	# 	#print(cart_id)
	# 	cart_obj = qs.first()
	# 	if request.user.is_authenticated and cart_obj.user is None:
	# 		print(cart_obj.user)
	# 		cart_obj.user = request.user 
	# 		cart_obj.save()
	# else:
	# 	cart_obj = Cart.objects.new(user=request.user)
	# 	request.session['cart_id'] = cart_obj.id
	# 	#cart_obj = Cart.objects.get(id=cart_id)
	#return render(request, "cart/home.html",{})
	# print(request.session) # on the request
	#print(dir(request.session))
	# request.session.set_expiry(300) # 5 minutes
	#key = request.session.session_key
	#print(key)
	#request.session['first_name'] = "Justin"  # this is setter
	#request.session['user'] = request.user #is an object but not json serializer json data
	#request.session['cart_id'] = 12 #set
	#request.session['user'] = request.user.username
	#return render(request, "cart/home.html", {})

	