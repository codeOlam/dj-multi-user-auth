from django.urls import path
from django.contrib.auth import views as auth_views


from accounts.views.views import (SignUpView,
									ActivateAccount, 
									LogInView,
									LogOutView)
from accounts.views.student_views import (StudentSignUpView, 
										StudentUpdateProfileView,
										StudentProfileView)


urlpatterns=[
	path('signup', SignUpView.as_view(), name='signup'),
	path('signup/as_student', StudentSignUpView.as_view(), name='std_signup'),
	# path('signup/as_teacher/', TeacherSignUpView.as_view(), name='teacher_signup'),
    path('email_activation/<uidb64>/<token>', ActivateAccount.as_view(), name='email_activation'),
	path('login', LogInView.as_view(), name='login'),
	path('logout', LogOutView.as_view(), name='logout'),
	path('student/<int:pk>/student_update_profile', StudentUpdateProfileView.as_view(), name='student_update_profile'),
	# path('teacher/<int:pk>/teacher_update_profile', TeacherUpdateProfileView.as_view(), name='teacher_update_profile'),
	path('student/<int:pk>', StudentProfileView.as_view(), name='teacher_profile'),
	# path('teacher/<int:pk>/', TeacherProfileView.as_view(), name='student_profile'),
]