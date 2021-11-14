from typing import Text
from django.core.checks.messages import Error
from django.shortcuts import render

from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 

from questions.models import Question
from questions.services import *
from questions.serializers import QuestionSerializer


@api_view(['GET', 'POST'])
def question_base_handler(request):
    try:
        if request.method == 'GET':
            questions_by_topics = get_questions_by_topics()
            return JsonResponse(questions_by_topics, safe=True)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            insert_question_by_text(data['text'])
            return HttpResponse("", status=201)        
        else: 
            return JsonResponse({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def question_detail_handler(request):
    try:
        return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def question_grammar_check_handler(request):
    try:
        return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def question_similiarity_check_handler(request):
    try:
        return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
