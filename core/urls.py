from django.urls import path
from .views import createJobPost, home, index, logout_user, recruiter_register, seeker_register

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('logout', logout_user, name='logout'),
    path('job/create/', createJobPost, name='create-job-post'),
    path('recruiter-registration', recruiter_register, name='recruiter_register'),
    path('seeker-registration', seeker_register, name='seeker_register')
]
