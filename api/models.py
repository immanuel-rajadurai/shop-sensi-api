from django.db import models
from django.db.models import JSONField

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True) 
    attributes = models.JSONField(default=dict, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
class QuestionList(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    question_list = JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return str(self.product)
    
class AnswerList(models.Model):
    question_list = models.ForeignKey(QuestionList, on_delete=models.CASCADE)
    answer_list = JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return str(self.question_list)