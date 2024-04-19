from unittest import mock
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Product, QuestionList, AnswerList
from api.ai_helpers import process_product_title, get_first_dict_string, parse_output, generate_attribute_value_pairs
from langchain.output_parsers import (
    PydanticOutputParser,
    OutputFixingParser,
    RetryWithErrorOutputParser,
)
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI
from openai import OpenAI
import openai
import json
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser, RetryWithErrorOutputParser
from pydantic import BaseModel, Field, validator
from typing import List
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.exceptions import OutputParserException, TracerException
from pydantic.v1.error_wrappers import ValidationError
import os
from api.tests.helpers import template_prompt
from unittest.mock import patch

class AiHelperTestCase(TestCase):

    def test_get_first_dict_string(self):
        input_string = '{"name": "Immanuel", "age": 30, "city": "London"}'
        expected_output = '{"name": "Immanuel", "age": 30, "city": "London"}'
        self.assertEqual(get_first_dict_string(input_string), expected_output)

        input_string = '{"name": "Ivana", "country": "Canada"}'
        expected_output = '{"name": "Ivana", "country": "Canada"}'
        self.assertEqual(get_first_dict_string(input_string), expected_output)

    def test_process_product_title_under_or_equal_to_250_chars(self):
        raw_title_short = "Short title"
        self.assertEqual(process_product_title(raw_title_short), raw_title_short)

        raw_title_long = "This is a very long product title that exceeds 250 characters. It needs to be truncated."
        expected_output = "This is a very long product title that exceeds 250 characters. It needs to be truncated."
        self.assertEqual(process_product_title(raw_title_long), expected_output)

        raw_title_exact = "Exactly 250 characters title. No truncation needed."
        self.assertEqual(process_product_title(raw_title_exact), raw_title_exact)

    def test_process_product_title_over_250_chars(self):
        long_product_title = ""

        for i in range(251):
            long_product_title = long_product_title + "a"
        
        self.assertEqual(process_product_title(long_product_title), long_product_title[:250])

    def test_generate_attribute_value_pairs(self):
        result = generate_attribute_value_pairs("Tennis Racket")
        self.assertTrue(type(result), dict)

    @patch("api.ai_helpers.get_first_dict_string")
    def test_generate_attribute_value_pairs_json_decode_error(self, mock_get_first_dict_string):
        mock_get_first_dict_string.return_value = "a"
        result = generate_attribute_value_pairs("Tennis Racket")
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    
class QuestionSet(BaseModel):
    question_set: List[str] = Field(description="the list of questions that I should ask myself before I purchase the product")

class TestParseOutput(TestCase):

    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(
            title="Sample Product",
            attributes={"color": "red", "size": "medium"}
        )

        self.product2 = Product.objects.create(
            title="Sample Product 2",
            attributes={"color": "red", "size": "medium"}
        )

        # Create a QuestionList associated with the product
        self.question_list = QuestionList.objects.create(
            product=self.product,
            question_list=[
                "question 1", "question 2"
            ]
        )

        self.parser = PydanticOutputParser(pydantic_object=QuestionSet)

        self.format_instructions = self.parser.get_format_instructions()
        self.llm = ChatOpenAI(temperature=0.0)
        self.prompt = ChatPromptTemplate.from_template(template=template_prompt)
        self.messages = self.prompt.format_messages(product_title="Tennis Racket",
                                format_instructions=self.format_instructions)
        self.output_raw = self.llm.invoke(self.messages)
        self.output_raw_text = self.output_raw.content

        self.raw_correct_output = """{"question_set":["question1", "question2"]}"""
        self.raw_incorrect_output = """{"question_set:["question1", "question2"]}"""
        self.product_title = "Tennis Racket"
        self.product_attributes = {"category":"Tennis Rackets"}

    def test_successful_parse(self):
        result = parse_output(self.parser, self.raw_correct_output, self.product_title, self.product_attributes, template_prompt)
        self.assertEqual(result, ["question1", "question2"])
        
    def test_output_fixing(self):
        result = parse_output(self.parser, self.raw_incorrect_output, self.product_title, self.product_attributes, template_prompt)
        self.assertTrue(type(result), list)

    @patch("langchain.output_parsers.OutputFixingParser.parse")
    def test_retry_parse(self, mock_fixed_parse):
        mock_fixed_parse.return_value = [{"question_set": "INCORRECT VALUE"}]
        result = parse_output(self.parser, self.raw_incorrect_output, self.product_title, self.product_attributes, template_prompt)
        self.assertTrue(type(result), list)
