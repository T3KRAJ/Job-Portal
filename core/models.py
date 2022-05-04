"In this module it provides what are the models present in the login it will shows"
"It was bulid by Sai Krishna And Tek Raj"
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, is_recruiter, is_seeker, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_recruiter=is_recruiter,
            is_seeker=is_seeker,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email


class SeekerProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )

    seeker = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default='M')
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    birthDate = models.DateField()
    current_job_role = models.CharField(max_length=255)
    current_company = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name


class RecruiterProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )

    recruiter = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default='M')
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_phone = models.IntegerField()

    def __str__(self):
        return self.first_name


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    sub_category_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name


class Job(models.Model):
    job_role = models.CharField(max_length=255)
    job_description = models.CharField(max_length=1000)
    organization = models.CharField(max_length=255)
    remuneration = models.IntegerField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, null=True)
    skill_required_1 = models.CharField(max_length=255)
    skill_required_2 = models.CharField(max_length=255)
    skill_required_3 = models.CharField(max_length=255, blank=True, null=True)
    skill_required_4 = models.CharField(max_length=255, blank=True, null=True)
    skill_required_5 = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.DateField()
    posted_date = models.DateField(auto_now_add=True)
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_role


class SeekerSkillset(models.Model):

    seeker = models.OneToOneField(SeekerProfile, on_delete=models.CASCADE)
    skill_1 = models.CharField(max_length=255)
    skill_2 = models.CharField(max_length=255, blank=True, null=True)
    skill_3 = models.CharField(max_length=255, blank=True, null=True)
    skill_4 = models.CharField(max_length=255, blank=True, null=True)
    skill_5 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.seeker.first_name


class Application(models.Model):

    APPLICATION_CHOICES = (
        ('A', 'ACTIVE'),
        ('S', 'SELECTED'),
        ('R', 'REJECTED'),
        {'I', 'Interview'},
    )

    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    seeker_name = models.CharField(max_length=255)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=1000)
    cv = models.FileField(upload_to='cvs/')
    matching_score = models.IntegerField()
    status = models.CharField(max_length=9,
                              choices=APPLICATION_CHOICES,
                              default='M')

    def __str__(self):
        return self.seeker.first_name


class Message(models.Model):
    message_type = models.CharField(max_length=1)
    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Interview(models.Model):

    interview_date = models.DateTimeField(auto_now_add=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
