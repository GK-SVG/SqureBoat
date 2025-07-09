
from django.urls import path
from mainapp.views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("post-job/", post_job, name="post-job"),
    path("get-recruiter-jobs/", get_recruiter_jobs, name="get-recruiter-jobs"),
    path("get-all-jobs/", get_all_jobs, name="get-all-jobs"),

    path("apply-to-job/", apply_to_job, name="apply-to-job"),
    path("applied-jobs/", get_applied_jobs, name="applied-jobs"),

    path("testLogin/", testLogin),

    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),


]
