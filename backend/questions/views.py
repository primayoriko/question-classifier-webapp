from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 

from questions.models import Question
from questions.services import *
from questions.serializers import QuestionSerializer


@api_view(['GET', 'POST'])
def question_base_handler(request):
    if request.method == 'GET':
        questions_by_topics = get_questions_by_topics()
        return JsonResponse(questions_by_topics, safe=True)

    elif request.method == 'POST':
        return JsonResponse({"status": "success"}, status=status.HTTP_201_CREATED)
        # question_data = JSONParser().parse(request)
        # tutorial_serializer = TutorialSerializer(data=tutorial_data)
        # if tutorial_serializer.is_valid():
        #     tutorial_serializer.save()
        #     return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        # return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else: 
        return JsonResponse({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def question_detail_handler(request):
    return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)

def question_grammar_check_handler(request):
    return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)

def question_similiarity_check_handler(request):
    return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
