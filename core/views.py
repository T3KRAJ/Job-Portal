"""_summary_
Views are created in this py file.
@Author: Tek Raj Joshi
"""
from datetime import date
from difflib import SequenceMatcher
from django.http import Http404
from django.shortcuts import redirect, render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout
from core.models import Application, Category, Interview, Job, Message, RecruiterProfile, SeekerProfile, SeekerSkillset, Subcategory
from .forms import Application_form, CreateJobForm, RecruiterProfileForm, SeekerProfileForm, SeekerRegistrationForm, RecruiterRegistrationForm, SkillForm
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


def index(request):
    if request.method == "POST":
        # User login view.
        form = AuthenticationForm(request, data=request.POST)
        email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # User login with email and password.
        if form.is_valid():
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                if request.user.is_recruiter:
                    try:
                        rec_profile = RecruiterProfile.objects.get(
                            recruiter_id=request.user.id)
                        last_login = request.user.last_login
                        message_list = Message.objects.filter(
                            recruiter_id=rec_profile.id).filter(date__gt=last_login)
                        if message_list:
                            messages.success(request, " Notification  :  You have new applications"
                                                      " for the job you posted since your last login")
                    except:
                        pass
                return redirect('home')
        else:
            args = {'form': form}
            return render(request, 'registration/index.html', args)
    else:
        form = AuthenticationForm
    args = {'form': form}
    return render(request, 'registration/index.html', args)

# User must be authenticated inorder to view home page.
@login_required
def home(request):
    return render(request, 'components/index.html')

def seeker_register(request):
    if request.method == 'POST':
        # Job seeker registration view.
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = SeekerRegistrationForm
    args = {'form': form}
    return render(request, 'registration/seeker_signup.html', args)

def recruiter_register(request):
    if request.method == 'POST':
        # Job recruiter registration view.
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = RecruiterRegistrationForm
    args = {'form': form}
    return render(request, 'registration/recruiter_signup.html', args)

@ login_required
def recruiterProfile(request):
    if request.method == 'POST':
        # Job recruiter profile creation view
        form = RecruiterProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            company_address = form.cleaned_data['company_address']
            company_phone = form.cleaned_data['company_phone']
            company_name = form.cleaned_data['company_name']
            try:
                profile = RecruiterProfile.objects.get(
                    recruiter_id=request.user.id)
                profile.first_name = first_name
                profile.last_name = last_name
                profile.gender = gender
                profile.company_address = company_address
                profile.company_phone = company_phone
                profile.company_name = company_name
                profile.save()

            except RecruiterProfile.DoesNotExist:

                RecruiterProfile.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    company_address=company_address,
                    company_phone=company_phone,
                    company_name=company_name,
                    recruiter_id=request.user.id
                ).save()
            form = RecruiterProfileForm(initial={'first_name': first_name, 'last_name': last_name,
                                                 'gender': gender, 'company_address': company_address,
                                                 'company_phone': company_phone,
                                                 'company_name': company_name})
        args = {'form': form}
        return render(request, 'components/recruiterprofile.html', args)
    else:
        if request.user.is_authenticated:
            recruiter = request.user.id
            try:
                profile = RecruiterProfile.objects.get(recruiter_id=recruiter)
                first_name = profile.first_name
                last_name = profile.last_name
                gender = profile.gender
                company_address = profile.company_address
                company_phone = profile.company_phone
                company_name = profile.company_name
            except:
                first_name = ""
                last_name = ""
                gender = ""
                company_address = ""
                company_phone = ""
                company_name = ""
            # Getting user details to show in profile
            form = RecruiterProfileForm(initial={'first_name': first_name, 'last_name': last_name,
                                                 'gender': gender, 'company_address': company_address,
                                                 'company_phone': company_phone,
                                                 'company_name': company_name})
            args = {'form': form}
            return render(request, 'components/recruiterprofile.html', args)


@ login_required
def seekerProfile(request):
    if request.method == 'POST':
        # Job seeker profile creation view
        form = SeekerProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            birthdate = form.cleaned_data['birthDate']
            current_job = form.cleaned_data['current_job_role']
            company = form.cleaned_data['current_company']
            try:
                profile = SeekerProfile.objects.get(seeker_id=request.user.id)
                profile.first_name = first_name
                profile.last_name = last_name
                profile.gender = gender
                profile.address = address
                profile.phone = phone
                profile.birthDate = birthdate
                profile.current_job = current_job
                profile.company = company
                profile.save()
            except SeekerProfile.DoesNotExist:
                SeekerProfile.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    address=address,
                    phone=phone,
                    birthDate=birthdate,
                    current_job_role=current_job,
                    current_company=company,
                    seeker_id=request.user.id
                ).save()
            form = SeekerProfileForm(initial={'first_name': first_name, 'last_name': last_name,
                                              'gender': gender, 'address': address, 'phone': phone, 'birthDate': birthdate,
                                              'current_job_role': current_job, 'current_company': company})
        args = {'form': form}
        return render(request, 'components/seekerprofile.html', args)
    else:
        if request.user.is_authenticated:
            seeker = request.user.id
            try:
                profile = SeekerProfile.objects.get(seeker_id=seeker)
                first_name = profile.first_name
                last_name = profile.last_name
                gender = profile.gender
                address = profile.address
                phone = profile.phone
                birthdate = profile.birthDate
                current_job = profile.current_job_role
                company = profile.current_company
            except:
                first_name = ""
                last_name = ""
                gender = ""
                address = ""
                phone = ""
                birthdate = ""
                current_job = ""
                company = ""
        # Getting user details to show in profile
            form = SeekerProfileForm(initial={'first_name': first_name, 'last_name': last_name,
                                              'gender': gender, 'address': address, 'phone': phone, 'birthDate': birthdate,
                                              'current_job_role': current_job, 'current_company': company})
            args = {'form': form}
            return render(request, 'components/seekerprofile.html', args)

def subcategory(request):
    category_id = request.GET.get('category')
    sub_category = Subcategory.objects.filter(category_id=category_id)
    return render(request, 'components/subcategory_drop_down.html', {'sub_category': sub_category})


def category(request):
    category_list = Category.objects.all()
    return render(request, 'components/category_drop_down.html', {'category': category_list})

@login_required
def createJobPost(request):
    if request.method == "POST":
        # Job post creation view.
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
            sub_category = form.cleaned_data['sub_category']
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
                    sub_category=sub_category,
                    recruiter_id=r_profile.id
                ).save()

                messages.success(request, 'Your Job was Created')
                return render(request, 'components/createjob.html')

            except RecruiterProfile.DoesNotExist:
                messages.warning(
                    request, 'You Must Complete Your Profile Before Creating Jobs')
                return render(request, 'components/createjob.html')

            except Exception as e:
                return render(request, 'components/createjob.html', {'form': form})

        else:
            messages.warning(
                request, "Job creation failed. Please make sure your form is complete and error free")
            return render(request, 'components/createjob.html', {'form': form})

    else:

        try:
            r_profile = RecruiterProfile.objects.get(
                recruiter_id=request.user.id)
            form = CreateJobForm
            args = {'form': form}
            return render(request, 'components/createjob.html', args)

        except RecruiterProfile.DoesNotExist:
            messages.warning(
                request, 'You Must Complete Your Profile Before Creating Jobs')
            return render(request, 'components/managejobs.html')

@login_required
def edit_job(request, id):
    if request.method == "POST":
        # Job post updation view.

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
            sub_category = form.cleaned_data['sub_category']
            try:
                job = Job.objects.get(id=id)
                job.job_role = job_role
                job.job_description = job_description
                job.organization = job_organization
                job.remuneration = job_remuneration
                job.location = job_location
                job.skill_required_1 = skill_required_1
                job.skill_required_2 = skill_required_2
                job.skill_required_3 = skill_required_3
                job.skill_required_4 = skill_required_4
                job.skill_required_5 = skill_required_5
                job.deadline = deadline
                job.category = category
                job.sub_category = sub_category
                job.save()
                messages.success(request, 'Your Job was Saved')
                form = CreateJobForm(initial={'job_role': job_role, 'job_description': job_description,
                                              'organization': job_organization, 'remuneration': job_remuneration,
                                              'location': job_location, 'skill_required_1': skill_required_1,
                                              'skill_required_2': skill_required_2, 'skill_required_3': skill_required_3, 'skill_required_4': skill_required_4, 'skill_required_5': skill_required_5, 'deadline': deadline,  'category': category, 'sub_category': sub_category.sub_category_name})
                args = {'form': form}
                return render(request, 'components/editjob.html', args)

            except Exception as e:
                messages.warning(
                    request, 'Job edit failed. Please make sure your form is complete and error free')
                return render(request, 'components/editjob.html', {'form': form})
        else:
            messages.warning(
                request, "Job edit failed. Please make sure your form is complete and error free")
            return render(request, 'components/editjob.html', {'form': form})
    else:
        try:
            job = Job.objects.get(pk=id)
            job_role = job.job_role
            job_description = job.job_description
            organization = job.organization
            remuneration = job.remuneration
            location = job.location
            skill_required_1 = job.skill_required_1
            skill_required_2 = job.skill_required_2
            skill_required_3 = job.skill_required_3
            skill_required_4 = job.skill_required_4
            skill_required_5 = job.skill_required_5
            category = job.category
            sub_category = job.sub_category
            deadline = job.deadline
            form = CreateJobForm(initial={'job_role': job_role, 'job_description': job_description,
                                          'organization': organization, 'remuneration': remuneration,
                                          'location': location, 'skill_required_1': skill_required_1,
                                          'skill_required_2': skill_required_2, 'skill_required_3': skill_required_3, 'skill_required_4': skill_required_4, 'skill_required_5': skill_required_5, 'deadline': deadline,
                                          'category': category, 'sub_category':
                                          sub_category.sub_category_name})
            args = {'form': form}
            return render(request, 'components/editjob.html', args)
        except Exception as e:
            messages.warning(request, 'No Such Job Exists')
            return render(request, 'components/editjob.html')

def search_for_jobs(request):
    if request.method == "GET":
        # Job search view.
        keyword = request.GET.get('keyword')
        if keyword == None or keyword == "":
            args = {'results': None}
            messages.warning(
                request, "Please input a  valid keyword for search")
            return render(request, 'components/index.html', args)
        search_by = request.GET.get('search_by')
        search_by_list = [1, 2, 3]
        if not search_by.isnumeric() or int(search_by) not in search_by_list:
            args = {'results': None}
            messages.warning(
                request, "Please select a valid value for search by")
            return render(request, 'components/index.html', args)
        category = request.GET.get('category')
        if not category:
            args = {'results': None}
            messages.warning(request, "Please select a valid category")
            return render(request, 'components/index.html', args)
        subcategory = request.GET.get('subcategory')
        if not subcategory:
            args = {'results': None}
            messages.warning(request, "Please select a valid subcategory ")
            return render(request, 'components/index.html', args)
        if search_by == "1":
            result = search_by_job_role(keyword, category, subcategory)
            args = {'results': result}
            if result == None:
                messages.warning(request, "No results found for your search")
            return render(request, 'components/index.html', args)
        if search_by == "2":
            result = search_by_location(keyword, category, subcategory)
            args = {'results': result}
            if result == None:
                messages.warning(request, "No results found for your search")
            return render(request, 'components/index.html', args)
        if search_by == "3":
            result = search_by_remuneration(keyword, category, subcategory)
            args = {'results': result}
            if result == None:
                messages.warning(request, "No results found for your search")
            return render(request, 'components/index.html', args)

def search_by_job_role(keyword, category, subcategory):
    keyword = keyword.strip()
    today = date.today()
    db_search = Job.objects.filter(category_id=category).filter(sub_category=subcategory).\
        filter(job_role__contains=keyword).filter(deadline__gte=today)
    if not db_search:
        return None
    return db_search

def search_by_location(keyword, category, subcategory):
    keyword = keyword.strip()
    today = date.today()
    db_search = Job.objects.filter(category_id=category).filter(sub_category=subcategory).\
        filter(location__contains=keyword).filter(deadline__gte=today)
    if not db_search:
        return None
    return db_search

def search_by_remuneration(keyword, category, subcategory):
    keyword = keyword.strip()
    try:
        today = date.today()
        length = len(keyword)
        keyword = int(keyword)
        keyword_range = (keyword, keyword+5000)
        db_search = Job.objects.filter(category_id=category).filter(sub_category_id=subcategory)\
            .filter(remuneration__range=keyword_range).filter(deadline__gte=today)\
            .order_by('remuneration')
        return db_search
    except:
        return None


@login_required
def job_details(request,jid):
    try:
        job = Job.objects.get(id=jid)
        if request.user.is_seeker:
            try:
                seekerprofile = SeekerProfile.objects.get(seeker=request.user)
                application = Application.objects.get(seeker=seekerprofile, job = job)
                status = application.status
                form = None

            except Exception:
                status = "T"
                form = Application_form

        else:
            status = "F"
            form = None

        args = {'job':job,
                'status':status,
                'form':form}

    except:
        messages.warning(request,"invalid request")
        args = {'job':None,
                'status':None,
                'form':None}
    print(status)
    return render(request,'components/job_details.html', args)

# User must be authenticated inorder to logout.
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

# User must be authenticated to apply for any job.
@login_required
def apply(request, jid):
    if request.method == "POST":
        form = Application_form(request.POST, request.FILES)
        job = Job.objects.get(id=jid)
        try:
            seekerProfile = SeekerProfile.objects.get(seeker=request.user)
            if form.is_valid():
                cv = request.FILES['cv']
                cover_letter = form.cleaned_data['cover_letter']
                score = matching_score(request, job, seekerProfile)
                application_id = Application.objects.create(
                    cv=cv,
                    cover_letter=cover_letter,
                    status='A',
                    seeker=seekerProfile,
                    matching_score=score,
                    job=job,
                    seeker_name=seekerProfile.first_name
                )
                application_id.save()
                job_application = Application.objects.get(id=application_id.id)
                Message.objects.create(
                    application=job_application,
                    recruiter=job.recruiter,
                    seeker=seekerProfile,
                    message_type='A',
                ).save()
                messages.success(
                    request, "You have sucessfully applied for this position")
                args = {'form': form,
                        'job': job}
                return render(request, 'components/job_details.html', args)
            else:
                messages.warning(
                    request, "Your application form had errors in it. Please re submit application")
                args = {'form': form,
                        'job': job,
                        'status': "T"}
                return render(request, 'components/job_details.html', args)
        except Exception as e:
            form = Application_form
            args = {
                form: form
            }
            messages.warning(request, "You need to add your skills.")
            return render(request, 'components/job_details.html', args)


    else:
        raise Http404("This is an invalid request")


def matching_score(request, job, seekerprofile):
    """_summary_
    A score is calculated based on similarity between job seeker's skill set and skills required 
    for the job using sequence matching library.
    Args:
        request (_type_)
        job (instance)
        seekerprofile (instance)

    Returns:
        int: matching score
    """

    job_skills = [job.skill_required_1, job.skill_required_2, job.skill_required_3,
                  job.skill_required_4, job.skill_required_5]
    job_skills = [i for i in job_skills if i is not None]
    user_skill_object = SeekerSkillset.objects.get(seeker=seekerprofile)
    user_skills = [user_skill_object.skill_1, user_skill_object.skill_2, user_skill_object.skill_3,
                   user_skill_object.skill_4, user_skill_object.skill_5]
    score_tab = []
    for item in job_skills:
        high_score = -1
        item.strip()
        if len(item) > 0:
            for user_skill in user_skills:
                score = SequenceMatcher(None, user_skill, item).ratio()
                if score > high_score:
                    high_score = score
        if high_score != -1:
            score_tab.append(high_score)
    total_score = sum(score_tab)
    length = len(score_tab)
    total_score /= length
    total_score *= 100
    return total_score

# User must be authenticated to view his/her job applications
@login_required
def my_applications(request):
    try:
        seekerprofile = SeekerProfile.objects.get(seeker_id=request.user.id)
        application_list = Application.objects.filter(
            seeker=seekerprofile).order_by('date')
        args = {'applications': application_list}

    except:
        application_list = []
        args = {'applications': application_list}

    return render(request, 'components/appliedjobs.html', args)

# User must be authenticated to view applications details of a particular job.
@login_required()
def applicant_details(request, jid, sid):
    try:
        seeker = SeekerProfile.objects.get(id=sid)
        application = Application.objects.get(id=jid)
        application_status = application.status

        args = {
            'seeker': seeker,
            'application': application,
            'status': application_status
        }
        return render(request, 'components/applicant_details.html', args)

    except SeekerProfile.DoesNotExist:
        messages.warning(
            request, 'This User does not exist in the system any more')
        return render(request, 'components/applicant_details.html')

    except Application.DoesNotExist:
        messages.warning(request, 'This application does not exists')
        return render(request, 'components/applicant_details.html')

# User must be authenticated to accept an applicant for a particular job application.
@login_required
def accept_applicant(request, aid):
    try:
        application = Application.objects.get(pk=aid)
        application.status = 'S'
        sid = application.seeker_id
        jid = application.job_id
        application.save()
        seeker = SeekerProfile.objects.get(id=sid)
        application_status = application.status
        args = {
            'seeker': seeker,
            'application': application,
            'status': application_status
        }
        messages.success(request, 'Applicant Selected')
        return render(request, 'components/applicant_details.html', args)
    except Exception as e:
        messages.warning(request, 'Invalid Request')
        return render(request, 'components/applicant_details.html')

# User must be authenticated to reject an applicant for a particular job application.
@login_required
def reject_applicant(request, aid):
    try:
        application = Application.objects.get(pk=aid)
        application.status = 'R'
        sid = application.seeker_id
        jid = application.job_id
        application.save()
        seeker = SeekerProfile.objects.get(id=sid)
        args = {
            'seeker': seeker,
            'application': application,
            'application_status': application.status
        }
        messages.success(request, 'Applicant Rejected')
        return render(request, 'components/applicant_details.html', args)
    except:
        messages.warning(request, 'Invalid Request')
        return render(request, 'components/applicant_details.html')

# User must be authenticated to set an interview call for a particular job application.
@login_required
def interview_call(request, aid):
    try:
        application = Application.objects.get(pk=aid)
        if application.status != 'I':
            application.status = 'I'
            application.save()
            sid = application.seeker_id
            jid = application.job_id
            job = Job.objects.get(id=jid)
            Interview.objects.create(
                application=application
            ).save()
            Message.objects.create(
                message_type='I',
                application=application,
                recruiter=job.recruiter,
                seeker=application.seeker,
            ).save()
            seeker = SeekerProfile.objects.get(id=sid)
            args = {
                'seeker': seeker,
                'application': application,
                'application_status': application.status
            }
            messages.success(request, 'Interview Call sent')
            return render(request, 'components/applicant_details.html', args)
        else:
            messages.warning(request, 'Invalid Request')
            return render(request, 'components/applicant_details.html')
    except Exception as e:
        messages.warning(request, 'Invalid Request')
        return render(request, 'components/applicant_details.html')

# User must be authenticated to view the applicants for a particular job.
@ login_required
def applications(request, id):
    try:
        application_list = Application.objects.filter(job_id=id)
        args = {'applications': application_list}
        return render(request, 'components/showapplicants.html', args)

    except Application.DoesNotExist:
        return render(request, 'components/showapplicants.html')

    except Exception as e:
        return render(request, 'components/showapplicants.html')


@ login_required
def skills(request):
    if request.method == "POST":
        #Job seeker's skills creation/updation view.
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_1 = form.cleaned_data['skill_1']
            skill_2 = form.cleaned_data['skill_2']
            skill_3 = form.cleaned_data['skill_3']
            skill_4 = form.cleaned_data['skill_4']
            skill_5 = form.cleaned_data['skill_5']
            try:
                seekerProfile = SeekerProfile.objects.get(
                    seeker_id=request.user.id)
                try:
                    skills = SeekerSkillset.objects.get(
                        seeker_id=seekerProfile.id)
                    skills.skill_1 = skill_1
                    skills.skill_2 = skill_2
                    skills.skill_3 = skill_3
                    skills.skill_4 = skill_4
                    skills.skill_5 = skill_5
                    skills.save()
                except SeekerSkillset.DoesNotExist:
                    SeekerSkillset.objects.create(
                        skill_1=skill_1,
                        skill_2=skill_2,
                        skill_3=skill_3,
                        skill_4=skill_4,
                        skill_5=skill_5,
                        seeker_id=seekerProfile.id
                    ).save()
                form = SkillForm(initial={'skill_1': skill_1, 'skill_2': skill_2, 'skill_3': skill_3,
                                          'skill_4': skill_4, 'skill_5': skill_5})
                args = {'form': form}
                return render(request, 'components/seekerskill.html', args)

            except SeekerProfile.DoesNotExist:
                messages.warning(
                    request, 'You Must Complete Your Profile Before Editing Skills')
                form = SkillForm()
                args = {'form': form}
                return render(request, 'components/seekerskill.html', args)
        else:
            args = {'form': form}
            messages.warning(
                request, 'Skills was not saved. There was some error in the form')
            return render(request, 'components/seekerskill.html', args)
    else:
        if request.user.is_authenticated:
            try:
                seekerProfile = SeekerProfile.objects.get(
                    seeker_id=request.user.id)
                skills = SeekerSkillset.objects.get(seeker_id=seekerProfile.id)
                skill_1 = skills.skill_1
                skill_2 = skills.skill_2
                skill_3 = skills.skill_3
                skill_4 = skills.skill_4
                skill_5 = skills.skill_5
                skills.save()
            except:
                skill_1 = ""
                skill_2 = ""
                skill_3 = ""
                skill_4 = ""
                skill_5 = ""
            form = SkillForm(initial={'skill_1': skill_1, 'skill_2': skill_2, 'skill_3': skill_3,
                                      'skill_4': skill_4, 'skill_5': skill_5})
            args = {'form': form}
            return render(request, 'components/seekerskill.html', args)

#Recruiter needs to be authenticated inorder to manage jobs.
@ login_required
def manage_jobs(request):
    try:
        r_profile = RecruiterProfile.objects.get(recruiter_id=request.user.id)
        job_list = Job.objects.filter(recruiter_id=r_profile.id)
        args = {'jobs': job_list}
    except:
        job_list = []
        args = {'jobs': job_list}
    return render(request, 'components/managejobs.html', args)


def search(request):
    return render(request, 'components/index.html')

