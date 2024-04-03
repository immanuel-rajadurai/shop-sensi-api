from .ai_question_generator import llm_generate_questions_2
from .models import Product
import json

class QuestionGenerator:

    def __init__(self, product:Product, number_of_questions:int=7):
        self.product_title = product.title
        self.product_attributes = product.attributes
        self.number_of_questions = number_of_questions
        self.template_prompt =   """I am considering purchasing a product, the title of the product is delimited by triple backticks. \
                                    Generate 7 questions that I should to ask myself before I purchase that product. \
                                    Ask the questions in yes/no format such that a "yes" answer to the question means that the purchase is rational for me and a "no" answer to the question means that the purchase is irrational for me. \
                                    Ask the questions in second person tense.  Refrain from asking questions relating to brand, budget or warranty.

                                    product title: ```{product_title}```

                                    {format_instructions}
                                """
        print("attribute value pairs within AQG are: ", self.product_attributes)

    def generate_questions(self) -> list:

        questions_list = llm_generate_questions_2(self.product_title,  self.template_prompt, self.product_attributes)
        return questions_list
