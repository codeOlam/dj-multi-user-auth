from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.urls import reverse_lazy, reverse



# import courses.models.Course

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves user
        """
        if not email:
        	raise ValueError('Must provide a valid email address')

        now = timezone.now()
        user    = self.model(
                        email=self.normalize_email(email),
                        date_joined=now,
                        last_login=now,
                        **extra_fields
                            ) 

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves superuser
        """
        user = self.model(
                          email = email,
                          **extra_fields                         
                          )
        user.set_password(password)
        user.is_admin =True
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user
 
sex_choices = [('MALE', 'Male'),
				('FEMALE', 'Female')]


class Users(AbstractUser):
	username 		= models.CharField(max_length=50, blank=True, null=True)
	email 			= models.EmailField(max_length=120, unique=True)
	other_names 	= models.CharField(max_length=50, blank=True, null=True)
	date_of_birth 	= models.DateField(null=True, blank=True)
	sex 			= models.CharField(max_length=6, choices=sex_choices, blank=True)
	address 		= models.CharField(max_length=255, blank=True)
	is_teacher 		= models.BooleanField(default=False)
	is_student 		= models.BooleanField(default=False)
	date_joined     = models.DateTimeField(auto_now_add=True)
	last_updated 	= models.DateTimeField(auto_now=True)


	objects = UserManager()

	USERNAME_FIELD = "email"
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email



class Student(models.Model):
	student 			= models.OneToOneField(Users, on_delete=models.CASCADE, related_name='on_p_stds', related_query_name='on_p_std')
	grade_year 			= models.DateField(blank=True)


	def __str__(self):
		return self.student.first_name+ " " +self.student.last_name


	def get_absolute_url(self):
		return reverse('student_profile', kwargs={'pk': self.student_id})


class Teacher(models.Model):
	teacher 			= models.OneToOneField(Users, on_delete=models.CASCADE, related_name='facilatators', related_query_name='facilitator')
	description 		= models.CharField(max_length=255, help_text='short description', blank=True)
	publication 		= models.TextField(blank=True)

	def __str__(self):
		return self.teacher.first_name+ " " + self.teacher.last_name

	def get_absolute_url(self):
		return reverse('teacher_profile', kwargs={'pk': self.teacher_id})