from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import *
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.contrib.auth.hashers import check_password


# Create your views here.

@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        email: str = request.data['email']
        password: str = request.data['password']
        user_type: str = request.data['user_type']

        if User.objects.filter(email=email).exists():
            return JsonResponse(status=400, data={"success": False, "message": "ACCOUNT_ALREADY_EXISTS"})
        
        if user_type not in ['candidate', 'recruiter']:
            return JsonResponse(status=400, data={"success": False, "message": "INVALID_USER_TYPE"})

        user = User.objects.create_user(
            email = email,
            password = password,
            user_type = user_type
        )

        # generate jwt tokens and send them back in response
        tokens = RefreshToken.for_user(user)

        return JsonResponse(status=200, data={
            'refresh_token': str(tokens),
            'access_token': str(tokens.access_token),
        })


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        email: str = request.data['email']
        password: str = request.data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(status=400, data={"success": False, "message": "USER_NOT_FOUND"})
        
        if check_password(password, user.password):
            # generate jwt tokens and send them back in response
            tokens = RefreshToken.for_user(user)

            return JsonResponse(status=200, data={
                'refresh_token': str(tokens),
                'access_token': str(tokens.access_token),
            })

        else:
            return JsonResponse(status=400, data={"success": False, "message": "INVALID_PASSWORD"})
        

@api_view(['POST'])
def logout(request):
    refresh_token: str = request.data['refresh']
    token = RefreshToken(refresh_token)
    token.blacklist()
    return JsonResponse(status=200, data={'message': "OK"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def testLogin(request):
    user: User = request.user
    return JsonResponse(status=200, data={"success":True, "message":"You are logged in"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_job(request):
    if request.method == "POST":
        user: User = request.user

        if user.user_type != "recruiter":
            JsonResponse(status=400, data={"success": False, "message": "INVALID_ACCESS"})

        job_title: str = request.data['job_title']
        job_desc: str = request.data['job_desc']

        job = PostedJob.objects.create(user=user, job_title=job_title, job_desc=job_desc)

        return JsonResponse(status=200, data={"success":True, "job_id":job.id, "message": "Job Created"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recruiter_jobs(request):
    if request.method == "GET":
        user: User = request.user
        
        jobs = PostedJobSerializer(PostedJob.objects.filter(user=user), many=True).data

        print("jobs--", jobs)

        return JsonResponse(status=200, data={"success":True, "jobs": jobs})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_jobs(request):
    if request.method == "GET":
        user: User = request.user
        jobs = PostedJobSerializer(PostedJob.objects.all(), many=True).data

        return JsonResponse(status=200, data={"success":True, "jobs": jobs})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_job(request):
    if request.method == "POST":
        user: User = request.user
        job_id: str = request.data['job_id']

        try:
            job = PostedJob.objects.get(id=job_id)
        except PostedJob.DoesNotExist:
            JsonResponse(status=400, data={"success": False, "message": "JOB_NOT_FOUND"})

        job, created = AppliedJob.objects.get_or_create(job=job, user=user)

        return JsonResponse(status=200, data={"success":True, "job_id":job.id, "message": "Applied to Job"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_applied_jobs(request):
    if request.method == "GET":
        user: User = request.user
        jobs = AppliedJobSerializer(AppliedJob.objects.filter(user=user), many=True).data
        return JsonResponse(status=200, data={"success":True, "jobs": jobs})

