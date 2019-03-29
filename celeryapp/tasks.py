"""
Module contain celery tasks
"""

from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import ProductData


@shared_task
def collect_data_task(id_data):
    """
    Create new product from products that get by id_data
    :param id_data: data of id lists
    :return: product id
    """
    return ProductData.objects.collect_product_data(id_data)


@shared_task
def remove_repetitions_task(product_id):
    """
    Create new product from product that get by product_id and remove product
    repetitions in product data.
    :param product_id: id of product object
    :return: product id
    """
    data_object = ProductData.objects.get(id=product_id)
    data_object.remove_repetitions()
    return product_id


@shared_task
def write_cheap_products_task(product_id):
    """
    Get product by product_id and rewrite product_data to cheap product list
    :param product_id: id of product object
    :return: product id
    """
    data_object = ProductData.objects.get(id=product_id)
    data_object.write_cheap_products()
    return product_id


@shared_task
def write_product_avr_prices_list_task(product_id):
    """
    Get product by product_id and rewrite product_data to average product list
    :param product_id: id of product object
    :return: product id
    """
    data_object = ProductData.objects.get(id=product_id)
    data_object.write_product_avr_prices_list()
    return product_id


@shared_task
def write_analog_list_of_product_list_task(product_id):
    """
    Get product by product_id and rewrite product_data
    to analog list of product list.
    :param product_id: id of product object
    :return: product id
    """
    data_object = ProductData.objects.get(id=product_id)
    data_object.write_analog_list_of_product_list()
    return product_id


@shared_task
def get_cheap_products_chain(id_data):
    """
    Celery chain when collect_data from id_data, remove_repetitions
    from this data and write_cheap_products_task.
    :param id_data: data of id lists
    """
    s = (
        collect_data_task.s(id_data).on_error(log_error.s()) |
        remove_repetitions_task.s().on_error(log_error.s()) |
        write_cheap_products_task.s().on_error(log_error.s())
    )
    s.delay()


@shared_task
def get_avg_prices_of_products_chain(id_data):
    """
    Celery chain when collect_data from id_data, remove_repetitions
    from this data and write_product_avr_prices_list_task.
    :param id_data: data of id lists
    """
    s = (
        collect_data_task.s(id_data).on_error(log_error.s()) |
        remove_repetitions_task.s().on_error(log_error.s()) |
        write_product_avr_prices_list_task.s().on_error(log_error.s())
    )
    s.delay()


@shared_task
def get_analog_list_of_product_list_chain(id_data):
    """
    Celery chain when collect_data from id_data, remove_repetitions
    from this data and write_analog_list_of_product_list_task.
    :param id_data: data of id lists
    """
    s = (
        collect_data_task.s(id_data).on_error(log_error.s()) |
        remove_repetitions_task.s().on_error(log_error.s()) |
        write_analog_list_of_product_list_task.s().on_error(log_error.s())
    )
    s.delay()


@shared_task
def log_error(request, exc, traceback):
    """
    Log errors data to product errors field
    :param request: celery task request data
    :param traceback: traceback
    """
    logs = '\n {0} \n\n ----- \n\n {1}'.format(request.task, traceback, )

    # Parse id list from request.args
    if isinstance(request.args[0], (list,)):
        id_list = request.args[0]
    else:
        id_list = request.args

    # Write logs
    for product_id in id_list:
        data_object = ProductData.objects.get(id=product_id)
        data_object.write_errors_logs(logs)
