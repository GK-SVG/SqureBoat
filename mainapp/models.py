from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email: str,
                    password: str,
                    user_type: str,
                    **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [
        ("candidate", "Candidate"),
        ("recruiter", "Recruiters"),
    ]

    objects = CustomUserManager()

    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100, choices=USER_TYPE)

    USERNAME_FIELD = 'email'

    # For Django auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email}"

class PostedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_desc = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.job_title}"
    
class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(PostedJob, on_delete=models.CASCADE)
