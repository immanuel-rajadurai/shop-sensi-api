from .ai_helpers import llm_generate_questions
from .models import Product
import json

class QuestionGenerator:

    def __init__(self, product:Product):
        self.product_title = product.title
        self.product_attributes = product.attributes

        self.template_prompt = """
            You are an intelligent shopping assistant that helps customers make smarter purchases. \

            A customer is considering purchasing a product, the title of the product is delimited by triple backticks. \
            The attributes of the product are delimited by triple backticks \
            Generate 7 questions that you will ask the customer to help them decide whether to purchase the product or not. \
            Ensure that you use the information about the product provided to you \n

            Ask each each question such that a "yes" answer to the question implies that the product is rational \
            for the customer to purchase and a "no" answer to the question implies that the product is irrational \
            for the customer to purchase. A rational purchase is defined as a purchase that best meets the customer's needs, \
            and is healthy for them in the long term \
            Ask the questions in second person tense.  Refrain from asking questions relating to budget, price, warranty, retailer, e-commerce company or reviews. \            
            Avoid asking the questions in a way that is biased to persuade the customer to buy the product. \
            
            product title: ```{product_title}``` \n
            product attributes: ```{product_attributes}``` \n

            {format_instructions}
        """


    def generate_questions(self) -> list:

        questions_list = llm_generate_questions(self.product_title,  self.template_prompt, self.product_attributes)
        return questions_list
