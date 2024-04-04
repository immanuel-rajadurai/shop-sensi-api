def process_product_title(raw_product_title): 
    if len(raw_product_title) > 250:
        return raw_product_title[:250]
    else:
        return raw_product_title