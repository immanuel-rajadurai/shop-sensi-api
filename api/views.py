from django.shortcuts import render
from rest_framework import generics
from .models import Product, QuestionList, AnswerList
from .serializers import ProductSerializer, QuestionSetSerializer
from .ai_helpers import generate_attribute_value_pairs
from .helpers import process_product_title
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .question_generator import QuestionGenerator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
@api_view(['GET'])
def get_questions_list_for_product(request, product_title):
    try:
        if product_title:

            print("product title is: ", product_title, " length is: ", len(product_title))

            processed_product_title = process_product_title(product_title)

            product = Product.objects.get(title=processed_product_title)

            question_list = QuestionList.objects.get(product=product)

            questions = question_list.question_list

            response_dict = {"questions":questions}

            # return Response(f"{questions}", status=status.HTTP_200_OK)
            return JsonResponse(response_dict, status=status.HTTP_200_OK)
        else:
            return Response("Missing 'product_title' in JSON data", status=status.HTTP_400_BAD_REQUEST)
        
    except Product.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@csrf_exempt
@api_view(['POST'])
def add_product(request):
    try:
        product_title = request.data.get('product_title')

        print("product title is", product_title)

        if product_title:

            if (Product.objects.filter(title=product_title).exists()): #if the product already exists within DB
                return Response(f"Product: {product_title} already exists within database", status=status.HTTP_400_BAD_REQUEST)

            processed_product_title = process_product_title(product_title)

            attribute_value_pairs = generate_attribute_value_pairs(processed_product_title)

            product = Product(title=processed_product_title, attributes=attribute_value_pairs)
            product.save()

            qg = QuestionGenerator(product, number_of_questions=7)
            generated_questions_list = qg.generate_questions()

            question_set = QuestionList(product=product, question_list=generated_questions_list)
            question_set.save()

            print("type of generated questions: ", type(generated_questions_list))

            response_dict = {"questions":generated_questions_list}
            print("response_dict: ", response_dict)

            # return Response(f"Generated questions: {question_set.question_list}", status=status.HTTP_200_OK)

            return JsonResponse(response_dict, status=status.HTTP_200_OK)
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

            question_list = QuestionList.objects.get(product=product)

            answer_set = AnswerList(question_list=question_list, answer_list=answers_list)
            answer_set.save()

            return Response(f"Answers {answers_list} saved")
        else:
            return Response("Missing 'product_title' in JSON data", status=status.HTTP_400_BAD_REQUEST)
    
    except Product.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print("EXCEPTION: ", type(e))
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)