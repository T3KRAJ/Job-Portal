from datetime import datetime
from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout

from core.models import Job, RecruiterProfile, SeekerProfile
from .forms import CreateJobForm, SeekerRegistrationForm, RecruiterRegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if form.is_valid():
            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                if user.is_recruiter:
                    messages.success(
                        request, " Notification  :  Logged in successfully!")
                    return redirect('home')
                elif user.is_seeker:
                    messages.success(
                        request, " Notification  :  Logged in successfully!")
                    return redirect('home')
                else:
                    args = {'form': form}
                    return render(request, 'registration/index.html', args)
        else:
            args = {'form': form}
            return render(request, 'registration/index.html', args)

    else:
        form = AuthenticationForm

    args = {'form': form}
    return render(request, 'registration/index.html', args)


@login_required
def home(request):
    if request.user.is_recruiter:
        user = RecruiterProfile.objects.get(recruiter=request.user)
        jobposts = Job.objects.filter(recruiter=user)
        context = {
            'user': user,
            'jobposts': jobposts
        }
    else:
        user = SeekerProfile.objects.get(seeker=request.user)
        current = datetime.datetime.now()
        jobposts = Job.objects.filter(deadline >= current)
        context = {
            'user': request.user,
            'jobposts': jobposts
        }

    return render(request, 'user/home.html', context)


def seeker_register(request):

    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    else:

        form = SeekerRegistrationForm

    args = {'form': form}

    return render(request, 'registration/seekerlogin.html', args)


def recruiter_register(request):

    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    else:
        form = RecruiterRegistrationForm

    args = {'form': form}

    return render(request, 'registration/recruiterlogin.html', args)


# @login_required
# def profileView(request, username):
#     user = get_object_or_404(User, username=username)
#     profile = Profile.objects.get(user=user)
#     posts = BlogPost.objects.filter(author=user)
#     context = {
#         'user': user,
#         'profile': profile,
#         'posts': posts,
#     }
#     return render(request, 'profile.html', context)


# @login_required
# def updateProfile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(
#             request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile', username=request.user)

#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#     return render(request, 'updateprofile.html', context)

@login_required
def createJobPost(request):

    if request.method == "POST":

        form = CreateJobForm(request.POST)

        if form.is_valid():

            job_role = form.cleaned_data['job_role']
            job_description = form.cleaned_data['job_description']
            job_organization = form.cleaned_data['organization']
            job_remuneration = form.cleaned_data['remuneration']
            job_location = form.cleaned_data['location']
            skill_required_1 = form.cleaned_data['skill_required_1']
            skill_required_2 = form.cleaned_data['skill_required_2']
            skill_required_3 = form.cleaned_data['skill_required_3']
            skill_required_4 = form.cleaned_data['skill_required_4']
            skill_required_5 = form.cleaned_data['skill_required_5']
            deadline = form.cleaned_data['deadline']
            category = form.cleaned_data['category']

            try:
                r_profile = RecruiterProfile.objects.get(
                    recruiter_id=request.user.id)

                Job.objects.create(
                    job_role=job_role,
                    job_description=job_description,
                    organization=job_organization,
                    remuneration=job_remuneration,
                    location=job_location,
                    skill_required_1=skill_required_1,
                    skill_required_2=skill_required_2,
                    skill_required_3=skill_required_3,
                    skill_required_4=skill_required_4,
                    skill_required_5=skill_required_5,
                    deadline=deadline,
                    category=category,
                    recruiter_id=r_profile.id
                ).save()

                messages.success(request, 'Your Job was Created!')
                return redirect('home')

            except RecruiterProfile.DoesNotExist:
                messages.warning(
                    request, 'You Must Complete Your Profile Before Creating Jobs!')
                return render(request, 'job/jobpost_form.html')

            except Exception as e:
                return render(request, 'job/jobpost_form.html', {'form': form})

        else:
            messages.warning(
                request, "Job creation failed. Please make sure your form is complete and error free!")
            return render(request, 'job/jobpost_form.html', {'form': form})

    else:

        try:
            r_profile = RecruiterProfile.objects.get(
                recruiter_id=request.user.id)
            form = CreateJobForm
            args = {'form': form}
            return render(request, 'job/jobpost_form.html', args)

        except RecruiterProfile.DoesNotExist:
            messages.warning(
                request, 'You Must Complete Your Profile Before Creating Jobs')
            return render(request, 'job/jobpost_form.html', args)


@login_required
def edit_job(request, id):
    data = get_object_or_404(Job, id=id)
    form = CreateJobForm(instance=data or None)

    if request.method == "POST":
        form = CreateJobForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('job_detail/id')
    context = {
        "form": form
    }
    return render(request, 'job/jobpost_form.html', context)


@login_required
def job_detail(request, jid):
    try:
        job = Job.objects.get(id=jid)
        context = {
            'job': job
        }
        return render(request, 'job/job_detail.html', context)

    except:
        messages.warning(request, "invalid request")
    return render(request, 'home')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
