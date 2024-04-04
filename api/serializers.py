from rest_framework import serializers
from .models import Product, QuestionList, AnswerList

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')

class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionList
        fields = ('__all__')


class AnswerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerList
        fields = ('__all__')