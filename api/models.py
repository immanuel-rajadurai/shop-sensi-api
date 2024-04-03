from django.db import models
from django.db.models import JSONField

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True) 
    attributes = models.JSONField(default=dict, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
class QuestionSet(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    questionsList = JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return str(self.product)
    
class AnswerSet(models.Model):
    questionSet = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    answers = JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return str(self.questionSet)