from django.urls import path, include
from .views import add_product, get_questions_list_for_product, add_answer

urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('add_answer/', add_answer, name='add_answer'),
    path('get_questions_list_for_product/<str:product_title>', get_questions_list_for_product, name='get_questions_list_for_product'),
]




# """
#     path('product/<int:pk>/', ProductDetail.as_view()),
#     path('questions/<int:pk>/', QuestionsDetail.as_view()),
#     path('generate_questions/<str:asin>/', QueryParamsView.as_view(), name='generate_questions'), #avoid using plurals
# """
