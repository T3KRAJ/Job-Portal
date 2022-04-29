from django.urls import path
from .views import createJobPost, edit_job, home, index, job_detail, logout_user, recruiter_register, seeker_register

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('logout', logout_user, name='logout'),
    path('job/create/', createJobPost, name='create-job-post'),
    path('job/update/<int:id>', edit_job, name='update-job-post'),
    path("job_detail/<int:jid>", job_detail, name="job_detail"),
    path('recruiter-registration', recruiter_register, name='recruiter_register'),
    path('seeker-registration', seeker_register, name='seeker_register')
]
