from django.contrib import admin
from .models import Product, QuestionList, AnswerList


# Register your models here.

admin.site.register(Product)
admin.site.register(QuestionList)
admin.site.register(AnswerList)