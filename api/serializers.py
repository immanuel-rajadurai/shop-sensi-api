from rest_framework import serializers
from .models import Product, QuestionSet, AnswerSet

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')

class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSet
        fields = ('__all__')


class AnswerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSet
        fields = ('__all__')