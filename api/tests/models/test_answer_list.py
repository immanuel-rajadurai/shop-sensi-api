# myapp/tests.py

from django.test import TestCase
from api.models import Product, QuestionList, AnswerList

class AnswerListTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Sample Product",
            attributes={"color": "red", "size": "medium"}
        )

        self.question_list = QuestionList.objects.create(
            product=self.product,
            question_list=[
                {"question": "Is it durable?", "answer": "Yes"},
                {"question": "What's the warranty?", "answer": "1 year"},
            ]
        )

        self.answer_list = AnswerList.objects.create(
            question_list=self.question_list,
            answer_list=[
                {"question": "Is it durable?", "answer": "Yes"},
                {"question": "What's the warranty?", "answer": "1 year"},
            ]
        )

    def test_answer_list_str(self):
        self.assertEqual(str(self.answer_list), "Sample Product")

    def test_answer_list_attributes(self):
        self.assertEqual(self.answer_list.answer_list, [
            {"question": "Is it durable?", "answer": "Yes"},
            {"question": "What's the warranty?", "answer": "1 year"},
        ])

    def test_answer_list_question_list(self):
        self.assertEqual(self.answer_list.question_list, self.question_list)

    def test_blank_answer_list(self):
        blank_answer_list = AnswerList.objects.create(question_list=self.question_list)
        self.assertEqual(blank_answer_list.answer_list, [])

    def test_null_answer_list(self):
        null_answer_list = AnswerList.objects.create(question_list=self.question_list, answer_list=None)
        self.assertIsNone(null_answer_list.answer_list)

