from django.contrib import admin
from .models import Product, QuestionSet, AnswerSet


# Register your models here.

admin.site.register(Product)
admin.site.register(QuestionSet)
admin.site.register(AnswerSet)