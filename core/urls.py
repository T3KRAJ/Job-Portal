from django.urls import path
from .views import accept_applicant, applicant_details, applications, apply, category, createJobPost, edit_job, home, index, interview_call, job_details, logout_user, manage_jobs, my_applications, recruiter_register, recruiterProfile, reject_applicant, search, search_for_jobs, seeker_register, seekerProfile, skills, subcategory

urlpatterns = [
    path("", index, name='index'),
    path("home", home, name='home'),
    path("search", search, name='search'),
    path("job_details/<int:jid>", job_details, name="job_details"),
    path("apply/<int:jid>", apply, name='apply'),
    path("see_applications", my_applications, name="my_applications"),
    path("seeker_register", seeker_register, name='seeker_register'),
    path("recruiter_register", recruiter_register, name='recruiter_register'),
    path("^search?", search_for_jobs, name="search_list"),
    path("seekerprofile", seekerProfile, name='seeker_profile'),
    path("recruiterprofile", recruiterProfile, name='recruiter_profile'),
    path("skills", skills, name='skills'),
    path("add_jobs", createJobPost, name='add_job'),
    path("manage_jobs", manage_jobs, name='manage_jobs'),
    path('job_edit/<int:id>', edit_job, name='job_edit'),
    path('applications/<int:id>', applications, name='applications'),
    path('applicant_details/<int:jid>/<int:sid>',
         applicant_details, name='applicant_details'),
    path('accept_applicant/<int:aid>',
         accept_applicant, name='accept_applicant'),
    path('reject_applicant/<int:aid>',
         reject_applicant, name='reject_applicant'),
    path('logout', logout_user, name='logout'),
    path('ajax/load_subcategory', subcategory, name='subcategory'),
    path('interview_call/<int:aid>', interview_call,
         name='send_interview_call'),
    path('ajax/load_category', category, name='category')
]
