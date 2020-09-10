from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import TextInput, DateInput, Select
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)


UserModel = get_user_model()

from accounts.models import Users


class LoginForm(forms.Form):
	"""
		Inheriting from django.contrib.auth.forms.AuthenticationForm base class
		to authenticate user, using email and password
	"""

	email		= forms.EmailField(label=("Email"), 
									max_length=254, 
									widget=forms.EmailInput(attrs={'class':'form-control',
										'autocomplete': 'email', 
										'autofocus': True, 'placeholder':'Email'})
									)
	password 	= forms. CharField(label=('Password'),
									strip=False,
									widget=forms.PasswordInput(attrs={'class':'form-control',
										'autocomplete':'current-password',
										'placeholder': 'Password'}),
									)
	error_messages = {
		'invalid_login': (
				"Please enter a correct %(email)s and password."
			),
		'inactive': ("This account is inactive or has been decativated."),

	}

	def __init__(self, request=None, *args, **kwargs):
		"""
			Set 'request' parameter to use by cutome authentication subclasses
			the form data comes in via **kwargs
		"""
		self.request 	= request
		self.user_cache	= None
		self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)


		super().__init__(*args, **kwargs)


	def clean(self):
		email 		= self.cleaned_data.get('email')
		password 	= self.cleaned_data.get('password')

		if email is not None and password:
			self.user_cache = authenticate(self.request, email=email, password=password)
			if self.user_cache is None:
				raise self.get_invalid_login_error()
			else:
				self.confirm_login_allowed(self.user_cache)

		return self.cleaned_data


	def confirm_login_allowed(self, user):
		"""
			Checks if user attempting to login is an active user
			if inactive login is rejected, if logged it returns None.
		"""

		if not user.is_active:
			raise forms.ValidationError(
					self.error_messages['inactive'],
					code='inactive',
				)

	def get_user(self):
		return self.user_cache


	def get_invalid_login_error(self):
		return forms.ValidationError(
				self.error_messages['invalid_login'],
				code='invalid_login',
				params={'email': self.email_field.verbose_name},
			)


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model 		= Users
		fields 		= ['first_name', 
						'last_name',
						'other_names', 
						'date_of_birth',
						'sex',
						'address', ]

		widgets		= {
			'first_name': TextInput(attrs={'class': 'form-control col-sm-10', 'placeholder':'First Name'}),
			'last_name': TextInput(attrs={'class': 'form-control col-sm-10', 'placeholder':'Last Name'}),
			'other_names': TextInput(attrs={'class': 'form-control col-sm-10', 'placeholder':'Other Name'}),
			'date_of_birth': DateInput(attrs={'class': 'form-control col-sm-10', 'placeholder':'Date of Birth'}),
			'sex': Select(attrs={'class': 'form-control col-sm-3'}),
			'address': TextInput(attrs={'class': 'form-control col-sm-10', 'placeholder':'Address'}),

		}	