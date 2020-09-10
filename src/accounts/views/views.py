from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django import forms
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.contrib.auth import get_user_model


userModel = get_user_model()

# Create your views here.
from accounts.models import Users
from accounts.forms.forms import LoginForm
from accounts.token import account_activation_token


class SignUpView(TemplateView):
	model 			= Users
	template_name 	= 'registration/signup.html'

	def post(self, request, *args, **kwargs):

		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			user.is_active=False
			user.save()

			current_site = get_current_site(request)
			site_name = current_site.name 
			domain = current_site.domain
			mail_subject = 'Account Activation Token'
			context = {'user':user,
						'domain': domain,
						'site_name':site_name,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': account_activation_token.make_token(user),
						}
			message = loader.render_to_string('registration/activation_email.html', context)
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()

			return TemplateResponse(request, 'registration/activate_email_prompt.html', {'page_title':'Email Confirmation'} )
		else:
			form = self.form_class()
			return TemplateResponse(request, self.template_name, {'form':form})


	def get_context_data(self, **kwargs):
		self.object = None
		context = super().get_context_data(**kwargs)

		return context




class ActivateAccount(TemplateView):
	success_url = reverse_lazy('login')
	activation_token = account_activation_token

	def get_user(self, uidb64):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = Users.objects.get(pk=uid)
		except(TypeError, ValueError, OverflowError, Users.DoesNotExist, ValidationError):
			user = None
		return user


	def dispatch(self, *args, **kwargs):
		assert 'uidb64' in kwargs and 'token' in kwargs

		self.user = self.get_user(kwargs['uidb64'])

		if self.user is not None:
			token = kwargs['token']
			if self.activation_token.check_token(self.user, token):
				self.user.is_active=True
				self.user.save()

				return TemplateResponse(self.request, 'registration/activate_email_done.html', {'page_title':'Email confirmation Successful',
																							'user':self.user } )
			else:
				return HttpResponse('Failed to Verify Email')
		return super().dispatch(*args, **kwargs)



class LogInView(LoginView):
	form_class 		= LoginForm
	template_name 	= 'registration/login.html'


class LogOutView(LogoutView):
	template_name 	= 'registration/loggedout.html'