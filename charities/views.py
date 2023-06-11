from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    pass


class CharityRegistration(APIView):
    pass


class Tasks(generics.ListCreateAPIView):
    pass


class TaskRequest(APIView):
    pass


class TaskResponse(APIView):
    pass


class DoneTask(APIView):
    pass