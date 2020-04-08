from django.http import Http404

from django.utils.http import is_safe_url

from django.contrib.auth import authenticate, login, get_user_model

from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm, RegisterForm, GuestForm

from .models import GuestEmail



from django.contrib import auth

from django.views.generic import CreateView, FormView  # ListView, DetailView
from .signals import user_logged_in

# from django.conf import settings

# User = settings.AUTH_USER_MODEL




def guest_register_view(request):
	form = GuestForm(request.POST or None)
	context = {
		"form": form
	}

	next_ 			= request.GET.get('next')
	next_post 		= request.POST.get('next')
	redirect_path 	= next_ or next_post or None

	if form.is_valid():
		email = form.cleaned_data.get("email")
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = new_guest_email.id

		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			return redirect("/register/")

	return redirect("/register/")




# def authenticate1(self, request, username=None, password=None, **kwargs):
#     # n.b. Django <2.1 does not pass the `request`

#     user_model = get_user_model()

#     if username is None:
#         username = kwargs.get(user_model.USERNAME_FIELD)

#     # The `username` field is allows to contain `@` characters so
#     # technically a given email address could be present in either field,
#     # possibly even for different users, so we'll query for all matching
#     # records and test each one.
#     users = user_model._default_manager.filter(
#         Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username)
#     )

#     # Test whether any matched user has the provided password:
#     for user in users:
#         if user.check_password(password):
#             return user
#     if not users:
#         # Run the default password hasher once to reduce the timing
#         # difference between an existing and a non-existing user (see
#         # https://code.djangoproject.com/ticket/20760)
#         user_model().set_password(password)





# def login_page(request):
# 	form = LoginForm(request.POST or None)
# 	context = {
# 		"form": form,
# 		"loginfail": "either username or password is wrong",
# 	}
# 	print("User Logged in")
# 	#print(request.user.is_authenticated()) #dont use () after is_authenticated because we are calling objects not function.
	# next_ 			= request.GET.get('next')
	# next_post 		= request.POST.get('next')
	# redirect_path 	= next_ or next_post or None

# 	if form.is_valid():
# 		# print(form.cleaned_data)
		# username = form.cleaned_data.get("username")
		# password = form.cleaned_data.get("password")
		# user = authenticate(request, username=username, password= password)


		# # if request.method=='POST':
		# # 	context["loginfail"] = "either username or password is wrong"
		# print(request.user.is_authenticated)
		# # if form == LoginForm(request.POST):
		# # 	context["loginfail"] = "either username or password is wrong"
		# if user is not None:
		# 	print(request.user.is_authenticated)
		# 	login(request, user)
		# 	try:
		# 		del request.session['guest_email_id']
		# 	except:
		# 		pass
				
		# 	# Redirect to a success page.
		# 	#context['form'] = LoginForm()
		# 	if is_safe_url(redirect_path, request.get_host()):
		# 		return redirect(redirect_path)
		# 	else:
		# 		return redirect("/")

# 		else:
# 			# Return an 'invalid login' error message.	
# 			print("Error and it is not a user")

# 	return render(request, "accounts/login.html", context)


# def logout_page(request):
# 	if request.user.is_authenticated is not None:
# 		print(request.user.is_authenticated)
# 		auth.logout(request)
# 		return redirect("/login")
# 	else:
# 		# Return an 'invalid login' error message.	
# 		print("it is not a user")

# 	return render(request, "accounts/login.html", context)



class LoginView(FormView):
	form_class = LoginForm
	# plus_context = dict()
	template_name = 'accounts/login.html'
	success_url = '/'


	def form_valid(self, form):	
		request 		= self.request		
		next_ 			= request.GET.get('next')
		next_post 		= request.POST.get('next')
		redirect_path 	= next_ or next_post or None

		username = form.cleaned_data.get("username") #asuming it as email
		password = form.cleaned_data.get("password")

		user = authenticate(request, username=username, password=password)


		# if not user.is_authenticated:
		# 	user = authenticate(request, username=username, password=password)
		# 	if not user.is_authenticated:
		#		try:
		# 			username = User.objects.get(email=email.lower()).username
		# 		except:
		#			pass
		#		user = authenticate(request, username=username, password=password)


		if user is not None:
			login(request, user)
			
			user_logged_in.send(user.__class__, instance=user, request= request)
				
			try:
				del request.session['guest_email_id']
			except:
				pass

			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		return super(LoginView, self).form_invalid(form)




class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'accounts/register.html'
	success_url = '/login/'



# User = get_user_model()
# def register_page(request):
# 	form= RegisterForm(request.POST or None)
# 	context = {
# 		"form": form
# 	}
# 	if form.is_valid():
		# print(form.cleaned_data)
		# username = form.cleaned_data.get("username")
		# email = form.cleaned_data.get("email")
		# password = form.cleaned_data.get("password")

		# new_user = User.objects.create_user(username, email, password)
# 		form.save()		
# 		print(new_user)
# 	return render(request, "accounts/register.html", context)


