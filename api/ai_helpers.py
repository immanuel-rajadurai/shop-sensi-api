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

OPEN_AI_KEY = "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"

os.environ["OPENAI_API_KEY"] = "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"

openai.api_key = OPEN_AI_KEY
# model_choice = "gpt-3.5-turbo-0125"
# client = OpenAI(api_key=OPEN_AI_KEY)

aqg_model_id="gpt-3.5-turbo-0125"
pae_model_id="ft:gpt-3.5-turbo-0125:personal:most-rel-pae-1:8yNmx9JN"


class QuestionSet(BaseModel):
    question_set: List[str] = Field(description="the list of questions that I should ask myself before I purchase the product")
 

def llm_generate_questions(product_title:str, template_prompt:str, product_attributes=None) -> list:

    parser = PydanticOutputParser(pydantic_object=QuestionSet)

    format_instructions = parser.get_format_instructions()

    llm = ChatOpenAI(temperature=0.0)

    prompt = ChatPromptTemplate.from_template(template=template_prompt)

    messages = prompt.format_messages(product_title=product_title,
                                format_instructions=format_instructions)
    
    output_raw = llm.invoke(messages)
    output_raw_text = output_raw.content

    return parse_output(parser, output_raw_text, product_title, template_prompt)


def parse_output(parser, raw_output, product_title, template_prompt):
    try: 
        parse = parser.parse(raw_output)
        print("NO NEED FOR FIXING PARSE")

        return dict(parse)["question_set"]
        
    except OutputParserException as e:
        print("ATTEMPTING TO FIX PARSE, caused by exception: ", e)
        output_fixer_parser = OutputFixingParser.from_llm(parser=parser,
                                         llm=ChatOpenAI())

    try:
        fixed_parse = output_fixer_parser.parse(raw_output)
        return dict(fixed_parse)["question_set"]
    
    except ValidationError as e:
        print("ATTEMPTING TO RETRY PARSE, caused by exception: ", type(e))
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=OpenAI(temperature=0), max_retries=3)

        prompt = PromptTemplate(
                    template=template_prompt,
                    input_variables=["product_title"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )
        
        prompt_value = prompt.format_prompt(product_title=product_title)
        retried_parse = retry_parser.parse_with_prompt(raw_output, prompt_value)

        return dict(retried_parse)["question_set"]


def get_first_dict_string(input_string):
    end_index = input_string.find('}') + 1
    return input_string[:end_index]


def generate_attribute_value_pairs(product_title):
    #testing
    #response_text = """{'category': 'Hard Drives', 'Type': 'SSD', 'Form Factor': '2.5 inch', 'Rotational Speed': '0.28"', 'Interface': 'SATA III'}"""

    messages = [{"role": "system", "content": "Your task is to extract product attribute value pairs from the following product title which is enclosed within triple quotes."}, 
                {"role": "user", "content": f" \n \"\"\"{product_title}\"\"\" \nPlease provide the attribute value pairs in JSON dictionary format, the first attribute must be \"category\" which is the lowest-level, most appropriate category of the product. Every value must be a string."}
               ]
    temperature = 0.05

    response = openai.chat.completions.create(model=pae_model_id, messages=messages, temperature=temperature)

    response_text = response.choices[0].message.content

    attribute_values_dict_string = get_first_dict_string(response_text).replace("'", "\"").replace("\"\"", "\"")

    try:
        return json.loads(attribute_values_dict_string)
    except json.JSONDecodeError:
        return {}

