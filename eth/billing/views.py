from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url

from .models import BillingProfile, Card

import stripe
stripe.api_key = "sk_test_ZoaMYzUyKgz9NDUJXoSzZ76V00vPUY2xTB"

STRIPE_PUB_KEY = 'pk_test_sDSJuqfqmePoOVohfLp65WoD00BzaBm3pW'


def payment_method_view(request):
	# if request.user.is_authenticated():
	# 	billing_profile = request.user.billingprofile
	# 	my_customer_id = billing_profile.customer_id
	
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	if not billing_profile:
		return redirect("/cart")

	next_url= None
	next_ = request.GET.get('next')
	if is_safe_url(next_, request.get_host()):
		next_url = next_
	# nextUrl = 
	return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url":next_url})


def payment_method_createview(request):
	if request.method=="POST" and request.is_ajax:		
		print(request.POST)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

		if not billing_profile:
			return HttpResponse({"message":"Cannot find this user"}, status_code=401)

		print(request.POST)
		token = request.POST.get("token")
		if token is not None:
			if billing_profile.customer_id:		
				customer = stripe.Customer.retrieve(billing_profile.customer_id)
				card_response = customer.sources.create(source=token)
				new_card_obj = Card.objects.add_new(billing_profile, card_response)
			else:
				return JsonResponse({"message": "customer id is empty and so id is not added!!"})
			print(new_card_obj)
			# post_text = request.POST.get('token')
			# print(post_text)
			return JsonResponse({"message": "success!!! your card is added!!"})
			#data = {"message": "Done"}
	raise HttpResponse("error", status_code=401) 