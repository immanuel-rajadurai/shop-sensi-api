from django.shortcuts import render
from rest_framework import generics
from .models import Product, QuestionSet, AnswerSet
from .serializers import ProductSerializer, QuestionSetSerializer
from .ai_question_generator import generate_attribute_value_pairs
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .question_generator import QuestionGenerator

@api_view(['GET'])
def get_questions_list_for_product(request, product_title):
    try:
        if product_title:

            product = Product.objects.get(title=product_title)

            questions_list_object = QuestionSet.objects.get(product=product)

            questions_list = questions_list_object.questionsList

            return Response(f"{questions_list}", status=status.HTTP_200_OK)
        else:
            return Response("Missing 'product_title' in JSON data", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@api_view(['POST'])
def add_product(request):
    try:
        product_title = request.data.get('product_title')
        if product_title:

            attribute_value_pairs = generate_attribute_value_pairs(product_title)

            product = Product(title=product_title, attributes=attribute_value_pairs)
            product.save()

            qg = QuestionGenerator(product, number_of_questions=7)
            questions_list = qg.generate_questions()

            question_set = QuestionSet(product=product, questionsList=questions_list)
            question_set.save()

            return Response(f"Generated questions: {question_set.questionsList}", status=status.HTTP_200_OK)
        else:
            return Response("Missing 'product_title' in JSON data", status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_answer(request):
    try:
        product_title = request.data.get('product_title')
        answers_list = request.data.get('answers')
        if product_title:

            product = Product.objects.get(title=product_title)

            questions_set_object = QuestionSet.objects.get(product=product)

            answer_set = AnswerSet(questionSet=questions_set_object, answers=answers_list)
            answer_set.save()

            return Response(f"Answers {answers_list} saved")
        else:
            return Response("Missing 'product_title' in JSON data", status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)