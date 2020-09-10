from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import TextInput, DateInput, Select
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

UserModel = get_user_model()

from accounts.models import Users, Student


class StudentSignUpForm(UserCreationForm):
	"""
		this form is responsible for user sign in
	"""
	email 			= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control',
											'placeholder':'Enter Valid Email',
											'autofocus':True, })
										)
	password1 		= forms.CharField(label='Password', 
										widget=forms.PasswordInput(attrs={'class':'form-control',
											'placeholder':'Enter Password'})
										 )
	password2 		= forms.CharField(label='Confirm Password', 
										widget=forms.PasswordInput(attrs={'class':'form-control',
											'placeholder':'Confirm Password'})
										)

	class Meta:
		model		= Users
		fields 		= ('email', 'is_student')


	def clean_password2(self):
		#Checks to validate if the two passwords are same
		password1 	= self.cleaned_data.get("password1")
		password2 	= self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Password Do not Match!")
		return password2


	def save(self, commit=True):
		user 	= super().save(commit=False)
		user.is_student=True
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user
