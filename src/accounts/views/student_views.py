from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django import forms
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

from accounts.models import Users, Student
from accounts.views.views import SignUpView
from accounts.forms.forms import LoginForm, ProfileUpdateForm
from accounts.forms.student_forms import StudentSignUpForm


class PermissionMixin(UserPassesTestMixin):
	def test_func(self):
		obj = self.get_object().id
		ru_id = self.request.user.id
		
		if self.request.user.is_authenticated and obj == ru_id:
			return True


class StudentSignUpView(SignUpView, CreateView):
	"""
	Handles the specific signup logic for users
	"""
	form_class 		= StudentSignUpForm
	template_name 	= 'registration/student_signup.html'
	success_url 	= '/'



class StudentProfileView(PermissionMixin, DetailView):
	model 					= Users
	context_object_name 	= 'std'
	template_name			= 'accounts/student/std_profile.html'

	#permission handling
	login_url			 = reverse_lazy('login')


	def get_context_data(self, **kwargs):
		context 	= super().get_context_data(**kwargs)

		#get id of currently logged in user by pk
		user_id		= self.kwargs.get('pk')

		#get extra context data/obj
		extra_fac = Student.objects.filter(student_id=user_id)

		context['extra_std'] = extra_std


		return context



class StudentUpdateProfileView(PermissionMixin, UpdateView):
	model 			= Users
	form_class		= ProfileUpdateForm
	template_name 	= 'accounts/student/std_profile_update.html'

	#permission handling
	login_url			 = reverse_lazy('login')


	def get_object(self, **kwargs):
		return self.model.objects.get(id=self.kwargs.get('pk'))

	def get_success_url(self):
		return reverse('fac_profile', args=[self.get_object().id])



	def post(self, request, *args, **kwargs):
		users 		= self.model.objects.get(email=self.get_object())
		StudentFormset = inlineformset_factory(Users, Student,
														fields=('grade_year',
																),
														can_delete=False
														)		

		formset 	= StudentFormset(request.POST, request.FILES, instance=users)
		form 		= self.form_class(request.POST, request.FILES, instance=users)
		if formset.is_valid():
			formset.save()
			form.save()

			return HttpResponseRedirect(self.get_success_url())

		else:
			formset = StudentFormset(instance=users)
			return TemplateResponse(request, self.template_name, {'form': self.form_class(instance=users),
																	'formset':formset})



	def get_context_data(self, **kwargs):
		context 	= super().get_context_data( **kwargs)
		users 		= self.model.objects.get(email=self.get_object())

		StudentFormset = inlineformset_factory(Users, Student,
									fields=('grade_year',
											),
									widgets={'description': forms.DateField(
											attrs={'class': 'form-control col-sm-10',
													'placeholder':'mm/dd/yyyy'}),
																			
									},
									can_delete=False
														)
		formset 	= StudentFormset(instance=users)

		context['formset'] = formset


		return context
