"""
Module contain celery app services
"""

from functools import reduce


def is_product_exist_in_list(product, product_list):
    """
    Return True if product in list or False if not
    :param product: product with search in list
    :param product_list: list of products
    :return: True if product in list or False if not
    """
    for iter_product in product_list:
        shop_concur = iter_product['shop'] == product['shop']
        product_concur = iter_product['product'] == product['product']
        series_concur = iter_product['series'] == product['series']
        if shop_concur and product_concur and series_concur:
            return True
    return False


def add_a_cheaper_product_to_list(product, product_list):
    """
    If product a cheaper in list clean list and add product to list,
    if list has a product with the same price save the list
    and add product to list.
    :param product: product with search in list
    :param product_list: list of products
    """
    if len(product_list) > 0:
        if product['price'] <= product_list[0]['price']:
            if product['price'] < product_list[0]['price']:
                del product_list[:]
            product_list.append(product)

    else:
        product_list.append(product)


def group_products_by_number(product_list):
    """
    Group product list by product number field
    :param product_list: list of products
    :return: splitted product list
    """
    result_dict = {}
    for iter_product in product_list:
        group = result_dict.get(iter_product['product'])
        if group:
            group.append(iter_product)
        else:
            result_dict[iter_product['product']] = [iter_product]
    return result_dict


def calculate_avr_price_by_shop(product_list):
    """
    Calculate average prices by shop to product
    :param product_list: products list
    :return: dict of average prices by shop
    """
    # Group by shop
    price_dict = {}
    for iter_product in product_list:
        shop = price_dict.get(iter_product['shop'])
        if shop:
            shop.append(iter_product['price'])
        else:
            price_dict[iter_product['shop']] = [iter_product['price']]

    # Calculate average price
    result_dict = {}
    for key, val in price_dict.items():
        result_dict[key] = int(reduce(lambda x, y: x + y, val) / len(val))

    return result_dict


def calculate_avr_price_by_shop_list(product_list):
    """
    Group product list by product number and
    calculate average prices in shop to products.
    :param product_list: list of products
    :return: dict of products list with average prices group by shop
    """
    result_dict = {}
    product_dict = group_products_by_number(product_list)
    for prod_num, product_list in product_dict.items():
        result_dict[prod_num] = calculate_avr_price_by_shop(product_list)
    return result_dict


def get_analog_list_of_product_list(product_list):
    """
    Return product dict and analogues of it
    :param product_list: list of product
    :return: list of product with analogues lists
    """
    result_dict = {}
    for iter_product in product_list:
        result_dict[iter_product['product']] = get_analog_list_of_product(
            iter_product, product_list
        )
    return result_dict


def get_analog_list_of_product(original_product, product_list):
    """
    Return product analogues list
    :param original_product: product whose analogues are sought
    :param product_list: list of product where analogues are sought
    :return: product analogues list
    """
    result_list = []
    for iter_product in product_list:
        if (original_product['series'] == iter_product['series'] and
                original_product['product'] != iter_product['product']):
            result_list.append(iter_product['product'])
    return result_list
