from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 

from questions.models import Question
# from questions.services import *
from questions.serializers import QuestionSerializer


@api_view(['GET', 'POST'])
def tutorial_list(request):
    pass
