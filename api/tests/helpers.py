template_prompt =   """I am considering purchasing a product, the title of the product is delimited by triple backticks. \
                                    Generate 7 questions that I should to ask myself before I purchase that product. \
                                    Ask the questions in yes/no format such that a "yes" answer to the question means that the purchase is rational for me and a "no" answer to the question means that the purchase is irrational for me. \
                                    Ask the questions in second person tense.  Refrain from asking questions relating to brand, budget or warranty.

                                    product title: ```{product_title}```

                                    {format_instructions}
                                """