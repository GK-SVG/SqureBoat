from rest_framework import serializers

from mainapp.models import *

class PostedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostedJob
        fields = ["id", "job_title", "job_desc"]


class AppliedJobSerializer(serializers.ModelSerializer):
    job_details = PostedJobSerializer(source='job', read_only=True)

    class Meta:
        model = AppliedJob
        fields = ["id", "job_details"]
