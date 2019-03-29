"""
Module contain models realizations
"""

import datetime
import json
import itertools

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models

from .services import is_product_exist_in_list, add_a_cheaper_product_to_list
from .services import calculate_avr_price_by_shop_list
from .services import get_analog_list_of_product_list


class ProductDataManager(models.Manager):
    """
    Product data manager
    """
    def get_json_data_by_id_list(self, id_list):
        """
        Return list of json data by id from id_list
        :param id_list: list of product id
        :return: list of json data
        """
        queryset = super()
        data = list(map(
            lambda product_id: queryset.get(id=product_id).get_json_data(),
            id_list
        ))
        return list(itertools.chain.from_iterable(data))

    def collect_product_data(self, id_list):
        """
        Collect data_file content of product list by id_list
        :param id_list: list of product id
        :return: product id
        """
        data = self.get_json_data_by_id_list(id_list)
        data_object = ProductData(data_name='collected')
        data_object.data_file.save(
            'collected_data.json',
            ContentFile(json.dumps(data))
        )
        return data_object.id


class ProductData(models.Model):
    """
    Product data model
    """
    data_name = models.CharField(blank=True, max_length=100)
    data_file = models.FileField(upload_to=settings.PRODUCT_DATA_DIR)
    errors = models.FileField(blank=True, upload_to=settings.PRODUCT_LOGS_DIR)

    objects = ProductDataManager()

    def save(self, *args, **kwargs):
        """
        Add data_name to object
        """
        if self.pk is None:
            self.data_name = '{}_{}'.format(self.data_name,
                                            str(datetime.datetime.now()))
        super().save(*args, **kwargs)

    def get_json_data(self):
        """
        Return data from file_data in json format
        :return: json data
        """
        return json.loads(self.data_file.read())

    def remove_repetitions(self):
        """
        Remove repetitions in data_file if exist
        """
        data = self.get_json_data()
        result_list = []
        for product in data:
            if not is_product_exist_in_list(product, result_list):
                result_list.append(product)
        self.data_name = '{}_{}'.format('unique', self.data_name)
        self.data_file.save(
            'unique_data.json',
            ContentFile(json.dumps(result_list))
        )

    def write_cheap_products(self):
        """
        Create data record with the cheapest product list
        :return: model id
        """
        data = self.get_json_data()
        product_list = []
        for iter_product in data:
            add_a_cheaper_product_to_list(iter_product, product_list)
        result_list = list(map(
            lambda product: product['product'],
            product_list
        ))
        self.data_name = '{}_{}'.format('cheap', self.data_name)
        self.data_file.save(
            'cheap_products.json',
            ContentFile(json.dumps(result_list))
        )
        return self.id

    def write_product_avr_prices_list(self):
        """
        Create data record with the average product list ordered by shops
        :return: model id
        """
        data = self.get_json_data()
        avg_prices = calculate_avr_price_by_shop_list(data)
        self.data_name = '{}_{}'.format('avg_price', self.data_name)
        self.data_file.save(
            'avg_prices_of_products.json',
            ContentFile(json.dumps(avg_prices))
        )
        return self.id

    def write_analog_list_of_product_list(self):
        """
        Write analog list of product list
        :return: model id
        """
        data = self.get_json_data()
        analogs = get_analog_list_of_product_list(data)
        self.data_name = '{}_{}'.format('analogs', self.data_name)
        self.data_file.save(
            'analogs_of_products.json',
            ContentFile(json.dumps(analogs))
        )
        return self.id

    def write_errors_logs(self, logs):
        """
        Write errors logs to file and save to data object
        :param logs: logs string
        :return:
        """
        self.errors.save(
            "errors.log",
            ContentFile(logs)
        )
        return self.id
