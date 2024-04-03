# from question_generator import QuestionGenerator
# from models import Product
# from ai_question_generator import llm_generate_questions_2


# product = Product(title="Notebook 500 pages hardback green", attributes={})

# qg = QuestionGenerator(product)

# questions_list = qg.generate_questions()

# print(questions_list)


































incorrectlyformatted = """{
                        "question_set": "j"
                         } 
                    """

misformatted = """{
                        "question_set": 
                            "Do you have a specific need or use case for the Baton?",
                            "Do you have experience using similar products to the Baton?",
                            "Are you confident in the quality and durability of the Baton?",
                            "Do you have the necessary skills or knowledge to use the Baton effectively?",
                            "Will the Baton contribute positively to your daily life or activities?",
                            "Is the size and weight of the Baton suitable for your preferences?",
                            "Are you comfortable with the price of the Baton in relation to its perceived value?"
                        ]
                    }"""

formatted = """{
                "question_set": [
                    "Do you have a specific need or use case for the Baton?",
                    "Do you have experience using similar products to the Baton?",
                    "Are you confident in the quality and durability of the Baton?",
                    "Do you have the necessary skills or knowledge to use the Baton effectively?",
                    "Will the Baton contribute positively to your daily life or activities?",
                    "Is the size and weight of the Baton suitable for your preferences?",
                    "Are you comfortable with the price of the Baton in relation to its perceived value?"
                ]
            }"""