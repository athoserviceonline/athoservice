from django import forms
from django.core.exceptions import ValidationError
#from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
import re 
from django.utils.safestring import mark_safe

from django.contrib.auth.forms import ReadOnlyPasswordHashField

# # from django.conf import settings

# # User = settings.AUTH_USER_MODEL
# #User = get_user_model()
# #from django.contrib.auth.models import User
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

User = get_user_model()



class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name','email',)

        # def __str__(self):
        #     return '{0}: {1}'.format(self.__class__.__name__, self.name)


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name','email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class GuestForm(forms.Form):
	email 	= forms.EmailField()

class ContactForm(forms.Form):
	fullname= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}))
	email= forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}))
	content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Your content"}))


class LoginForm(forms.Form):
	username = forms.CharField(label=mark_safe('Username or Email'))
	password = forms.CharField(widget= forms.PasswordInput,label=mark_safe('Password'))




class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name','email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        #user.active= False   # send confirmation email      
        if commit:
            user.save()
        return user



# class RegisterForm(forms.Form):
# 	username = forms.CharField()
# 	email= forms.EmailField(widget=forms.EmailInput())
# 	password = forms.CharField(widget= forms.PasswordInput)
# 	password2 = forms.CharField(label='confirm password',widget= forms.PasswordInput)
# 	phone_number = forms.IntegerField(label='phone number', widget=forms.TextInput(attrs={ 'max_length': 14, 'required': True, } ), )

# 	def clean_username(self):
# 		username = self.cleaned_data.get('username')
# 		old_user = User.objects.filter(username=username)
# 		if old_user.exists():
# 			raise forms.ValidationError("Username is taken")
# 		return username

# 	def clean_email(self):
# 		email = self.cleaned_data.get('email')
# 		old_email = User.objects.filter(email=email)
# 		if old_email.exists():
# 			raise forms.ValidationError("Email is taken")
# 		return email

# 	def clean_password(self):
# 		password = self.cleaned_data.get('password')
# 		if(len(password)<5): 
# 			raise forms.ValidationError("Password must have minimum 5 characters.")
# 		elif not re.search("[a-z]", password): 
# 			raise forms.ValidationError("Password must have a small character.")
# 		elif not re.search("[A-Z]", password): 
# 			raise forms.ValidationError("Password must have a capital character.")
# 		elif not re.search("[$&+,:;=?@#|'<>.-^*()%!]", password): 
# 			raise forms.ValidationError("Password must have a special character.")
# 		elif not re.search("[0-9]", password): 
# 			raise forms.ValidationError("Password must have numbers.")
# 		else: 
# 			return password 

# 	def clean(self):
# 		data = self.cleaned_data
# 		password = self.cleaned_data.get('password')
# 		password2= self.cleaned_data.get('password2')
# 		if password2 != password:
# 			raise forms.ValidationError("Password must match.")
# 		return data

						
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