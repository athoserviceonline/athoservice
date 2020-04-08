from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re 
from django.utils.safestring import mark_safe

User = get_user_model()

class ContactForm(forms.Form):
	fullname= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}))
	email= forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}))
	content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Your content"}))

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if not "gmail.com" in email:
			raise ValidationError("Email has to be gmail.com")
		return email 

	def clean_content(self):
		content = self.cleaned_data.get("content")
		if len(content) <=5:
			raise ValidationError("content must be more.. more than 5 letters")

class LoginForm(forms.Form):
	username = forms.CharField(label=mark_safe('username'))
	password = forms.CharField(widget= forms.PasswordInput,label=mark_safe('Password'))


class RegisterForm(forms.Form):
	username = forms.CharField()
	email= forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget= forms.PasswordInput)
	password2 = forms.CharField(label='confirm password',widget= forms.PasswordInput)
	phone_number = forms.IntegerField(label='phone number', widget=forms.TextInput(attrs={ 'max_length': 14, 'required': True, } ), )

	def clean_username(self):
		username = self.cleaned_data.get('username')
		old_user = User.objects.filter(username=username)
		if old_user.exists():
			raise ValidationError("Username is taken")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		old_email = User.objects.filter(email=email)
		if old_email.exists():
			raise ValidationError("Email is taken")
		return email

	def clean_password(self):
		password = self.cleaned_data.get('password')
		if(len(password)<5): 
			raise ValidationError("Password must have minimum 5 characters.")
		elif not re.search("[a-z]", password): 
			raise ValidationError("Password must have a small character.")
		elif not re.search("[A-Z]", password): 
			raise ValidationError("Password must have a capital character.")
		elif not re.search("[$&+,:;=?@#|'<>.-^*()%!]", password): 
			raise ValidationError("Password must have a special character.")
		elif not re.search("[0-9]", password): 
			raise ValidationError("Password must have numbers.")
		else: 
			return password 

	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		password2= self.cleaned_data.get('password2')
		if password2 != password:
			raise ValidationError("Password must match.")
		return data

						
# class PhoneOTP(models.Model):
# 	phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$', message ="Phone Number must be entered in the format: '+919535466453'. Up to 14 digits")
# 	phone = models.CharField(validators=[phone_regex], max_length=17, unique = True)
# 	otp = models.CharField(max_length=9 , blank= True, null= True)
# 	count = models.IntegerField(default =0, help_text = 'Number of otp sent')
# 	validated = models. BooleanField(default=False, help_text="If it is true, that means user have validate otp correctly in second API")

# 	def __str__(self):
# 		return str(self.phone) + 'is sent' + str(self.otp)









	# def clean_email(self):
	# 	email = self.cleaned_data.get("email")
	# 	if not "gmail.com" in email:
	# 		raise forms.ValidationError("Email has to be gmail.com")
	# 	return email 