import requests
import json


def get_api_data(entered_asin):
    params = {
        'api_key': '95BB5FE6AE904F3A8B8FD9C94C2EB732',
        'type': 'product',
        'amazon_domain': 'amazon.co.uk',
        'asin': entered_asin
    }
    # make the http GET request to ASIN Data API
    api_result = requests.get('https://api.asindataapi.com/request', params)
    return json.dumps(api_result.json())


def get_product_data_from_amazon(entered_asin):
    response_json = get_api_data(entered_asin)

    response_dict = json.loads(response_json)

    categories_tree_list = response_dict["product"]["bestsellers_rank"]

    price =  response_dict["product"]["buybox_winner"]["price"]["value"]

    return [categories_tree_list[-1]["category"], price]

