from django.http import Http404,JsonResponse,HttpResponse

from django.contrib.auth import authenticate, login, get_user_model 
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ContactForm

from django.contrib import auth

# from analytics.signals import object_viewed_signal

from analytics.mixins import ObjectViewMixin


from django.views.generic import ListView, DetailView

from cart.models import Cart

from .models import Product

#from . import forms
#from django.core.mail import send_mail,EmailMessage
#from django.conf import settings

# Create your views here.
def HomeView(request):
	
	#if not request.user.is_authenticated:
	#	return redirect('/login')
	#print(request.session.get("first_name","unknown")) #it is getter
	context = {
	"title":"Hello World!! this is home page",
	"content":"Home page is waiting for u",
	"premium_content":"Yeahhh it is a premium content"
	}
	# if request.user.is_authenticated:
	# 	context["premium_content"] = "Yeahhh it is a premium content"
	return render(request,'homepage.html', context)

def AboutView(request):
	context = {"title":"Hello World!! this is About page",
	 "content":"About page is waiting for u"
	 }
	return render(request,'homepage.html', context)

def ContactView(request):
	contact_form = ContactForm()
	context = {"title":"Hello World!! this is Contact page",
	"content":"Contact page is waiting for u",
	"form": contact_form
	# "brand": "new Brand Name"
	}

	if request.method=='POST':
		contact_form=ContactForm(request.POST)
		if contact_form.is_valid():
			print(contact_form.cleaned_data)
			if request.is_ajax():
				return JsonResponse({"message":"Thank You for your submission..:-)"})

		if contact_form.errors:
			# print(contact_form.cleaned_data)
			errors = contact_form.errors.as_json()
			if request.is_ajax():
				return HttpResponse(errors, status=400, content_type='application/json')
	# if request.method=='POST':
	# 	contact_form=ContactForm(request.POST)
	# 	if contact_form.is_valid():
	# 		print(contact_form.cleaned_data)
	# 		return render(request,'homepage.html', {"title":"Thank you for submitting the data","content":"contact page is waiting for u and shortly we are contacting u"})

	return render(request,'contact/ContactView.html', context)


# class ProductFeaturedListView(ListView):
# 	# queryset = Product.objects.all()
# 	template_name = "products/list.html"

# 	def get_queryset(self, *args, **kwargs):
# 		request = self.request
# 		return Product.objects.featured()



# class ProductFeaturedDetailView(ObjectViewMixin, DetailView):
# 	#queryset = Product.objects.all()
# 	template_name = "products/featured-detail.html"

	# get_object()
# 	def get_queryset(self, *args, **kwargs):
# 			request = self.request
# 			return Product.objects.featured()



	# def get_object(self, *args, **kwargs):
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')

	# 	instance = Product.objects.get_by_id(pk)
	# 	if instance is None:
	# 		raise Http404("Product doesn't exist")

	# 	return instance



class ProductListView(ListView):
	# queryset = Product.objects.all()
	template_name = "products/list.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all()		

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView,self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context


# def product_list_view(request):
# 	queryset = Product.objects.all()
# 	context = {
# 	'object_list': queryset
# 	}
# 	return render(request, "products/list.html", context)


# class ProductDetailSlugView(ListView):
# 	queryset = Product.objects.all()
# 	template_name = "products/list.html"	

	
class ProductDetailSlugView(ObjectViewMixin ,DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"	

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')

		#instance = get_object_or_404(Product, slug=slug, active = True)
		try:
			instance = Product.objects.get(slug=slug, active = True)
		except Product.DoesNotExist:
			raise Http404("Not Found..")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active = True)
			instance = qs.first()
		except:
			raise Http404("Uhhhmm..")
		# object_viewed_signal.send(instance.__class__, instance= instance, request=request) #view is the class
		return instance

# class ProductDetailView(ObjectViewMixin ,DetailView):
# 	#queryset = Product.objects.all()
# 	template_name = "products/detail.html"

# 	# def get_context_data(self, *args, **kwargs):
# 	# 	context = super(ProductDetailView,self).get_context_data(*args, **kwargs)
# 	# 	print(context)
# 	# 	return context

# 	def get_object(self, *args, **kwargs):
# 		request = self.request
# 		pk = self.kwargs.get('pk')

# 		instance = Product.objects.get_by_id(pk)
# 		if instance is None:
# 			raise Http404("Product doesn't exist")

# 		return instance

# def product_detail_view(request, pk=None, *args, **kwargs):
# 	#instance = Product.objects.get(pk=pk) #id

# 	#instance = get_object_or_404(Product, pk=pk)


# 	# try: 
# 	# 	instance = Product.objects.get(id=pk)
# 	# except Product.DoesNotExist:
# 	# 	print('no product here')
# 	# 	raise Http404("Product doesnt exist")
# 	# except:
# 	# 	print("huh?..")

# 	instance = Product.objects.get_by_id(pk)
# 	if instance is None:
# 		raise Http404("Product doesn't exist")

# 	# print(instance)

# 	# qs = Product.objects.filter(id=pk)
# 	# if qs.exists() and qs.count() == 1:
# 	# 	instance = qs.first()
# 	# else:
# 	# 	raise Http404("product doesn't exist")

# 	context = {
# 	'object': instance
# 	}
# 	return render(request, "products/detail.html", context)






 

# class ValidateOTP(APIView):
# 	'''if you have otp post a request with phone and that otp and you will be redirected to set the password
# 	'''

# 	def post(self, request, *args, **kwargs):
# 		phone = request.data.get('phone', False)
# 		otp_sent = request.data.get('otp', False)

# 		if phone & otp_sent:
# 			old = PhoneOTP.objects.filter(phone_iexact = phone)
# 			if old.exists():
# 				old = old.first()
# 				otp = old.otp
# 				if str(otp_sent) == str(otp):
# 					old.validated = True
# 					old.save()
# 					return Response({
# 						'status': True,
# 						'detail': 'OTP Matched, Please proceed for registration'
# 						})
# 				else:
# 					return Response({
# 						'status': False,
# 						'detail': 'OTP INCORRECT'
# 						})	
# 			else:
# 				return Response({
# 					'status': False,
# 					'detail': 'First proceed via sending otp request'
# 					})
# 		else:
# 				return Response({
# 					'status': False,
# 					'detail': 'Please provide both phone and OTP for validation'
# 					})


# def ContactView(request): 
# 	contact_form = ContactForm(request.POST or None)
# 	context = {"title":"Hello World!! this is Contact page","content":"Contact page is waiting for u","form": contact_form}
# 	if contact_form.is_valid():
# 		print(contact_form.cleaned_data)
# 	return render(request,'contact/ContactView.html', context)













	# if request.method == "POST":
	# 	print(request.POST)
	# 	print(request.POST.get("fullname"))
	# 	print(request.POST.get("email"))
	# 	print(request.POST.get("content"))


# def RegisterView(request):
#     form=forms.RegisterForm()
#     if request.method=='POST':
#         form=forms.RegisterForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             print("Data inserted into Database Successfullly..!!")

#             name= form.cleaned_data['name']
#             # personimage = form.cleaned_data['personimage']
#             mail = form.cleaned_data['email']
#             phone = form.cleaned_data['phone']
#             reason = form.cleaned_data['reason']
#             gender= form.cleaned_data['gender']

#             send_mail('want to take appointment for '+str(mail),
#                 "name : "+str(gender)+" "+str(name)+"\n"
#                 # "person's photo :"+ attach(personimage)+"\n"
#                 "email : "+str(mail)+"\n"
#                 "phone no : "+str(phone)+"\n"
#                 "reason to meet : "+ str(reason),
#                 settings.EMAIL_HOST_USER,
#                 ['studentgcek@gmail.com'],
#                 fail_silently=False )
#             return thankView(request)


#     return render(request,'myapp/home.html',{'form':form})