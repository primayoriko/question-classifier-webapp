from typing import Text
from django.core.checks.messages import Error
from django.shortcuts import render

from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 

from questions.models import Question
from questions.serializers import QuestionSerializer
from questions.services import *


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

@api_view(['GET'])
def question_detail_handler(request, id):
    try:
        question_detail = get_question_detail_by_id(id)
        return JsonResponse(question_detail, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def question_grammar_check_handler(request):
    try:
        data = JSONParser().parse(request)
        grammar_correctness = check_grammar(data['text'])
        return JsonResponse({"grammar_correctness": grammar_correctness}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def similiar_question_check_handler(request):
    try:
        data = JSONParser().parse(request)
        similiar_questions = check_all_similiar(data['text'])
        return JsonResponse({"similiar_questions": similiar_questions}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse({"message": "something unexcepted happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
