"""
Module contain test cases of json services
"""

from django.test import TestCase

from ..services import add_a_cheaper_product_to_list
from ..services import is_product_exist_in_list, group_products_by_number
from ..services import calculate_avr_price_by_shop_list
from ..services import calculate_avr_price_by_shop
from ..services import get_analog_list_of_product
from ..services import get_analog_list_of_product_list


class ServicesTestCase(TestCase):
    """
    Test cases of services
    """
    def setUp(self):
        pass

    def test_is_product_exist_in_list(self):
        """
        Test that is_product_exist_in_list work correctly
        """
        product_list = [
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "A",
            },
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 500,
                "series": "B",
            }

        ]

        self.assertTrue(is_product_exist_in_list(
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "A",
            },
            product_list
        ))
        self.assertTrue(is_product_exist_in_list(
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 500,
                "series": "B",
            },
            product_list
        ))
        self.assertTrue(is_product_exist_in_list(
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 1000,
                "series": "B",
            },
            product_list
        ))
        self.assertFalse(is_product_exist_in_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 1000,
                "series": "A",
            },
            product_list
        ))
        self.assertFalse(is_product_exist_in_list(
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "B",
            },
            product_list
        ))

    def add_a_cheaper_product_to_list(self):
        """
        Test that a_cheaper_product_to_list work correctly
        """
        product_list = []

        result_list = add_a_cheaper_product_to_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 100,
                "series": "A",
            },
            product_list
        )
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0]['price'], 100)

        result_list = add_a_cheaper_product_to_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 100,
                "series": "A",
            },
            product_list
        )
        self.assertEqual(len(result_list), 2)
        self.assertEqual(result_list[0]['price'], 100)

        result_list = add_a_cheaper_product_to_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 200,
                "series": "A",
            },
            product_list
        )
        self.assertEqual(len(result_list), 2)
        self.assertEqual(result_list[0]['price'], 100)

        result_list = add_a_cheaper_product_to_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 50,
                "series": "A",
            },
            product_list
        )
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0]['price'], 50)

        result_list = add_a_cheaper_product_to_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 10,
                "series": "A",
            },
            product_list
        )
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0]['price'], 10)

        result_list = add_a_cheaper_product_to_list(
            {
                "shop": "DNS",
                "product": 2,
                "price": 1000,
                "series": "A",
            },
            product_list
        )
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0]['price'], 10)

    def test_group_products_by_number(self):
        """
        Test that group_products_by_number work correctly
        """
        product_list = [
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "A",
            },
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "AB",
            },
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 500,
                "series": "B",
            },
            {
                "shop": "DNS",
                "product": 2,
                "price": 500,
                "series": "B",
            },
            {
                "shop": "DNS",
                "product": 3,
                "price": 500,
                "series": "CB",
            }

        ]
        result = group_products_by_number(product_list)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[1]), 2)
        self.assertEqual(len(result[2]), 2)
        self.assertEqual(len(result[3]), 1)

        self.assertEqual(result[1][0]['product'], 1)
        self.assertEqual(result[1][1]['product'], 1)
        self.assertEqual(result[3][0]['product'], 3)

    def test_calculate_avr_price_by_shop(self):
        """
        Test that calculate_avr_price_by_shop work correctly
        """
        product_list = [
            {
                "shop": "DNS",
                "product": 1,
                "price": 600,
                "series": "A",
            },
            {
                "shop": "DNS",
                "product": 1,
                "price": 100,
                "series": "AB",
            },
            {
                "shop": "Technopoint",
                "product": 1,
                "price": 1000,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 1,
                "price": 400,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 1,
                "price": 100,
                "series": "B",
            }
        ]
        result = calculate_avr_price_by_shop(product_list)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result['DNS'], 350)
        self.assertEqual(result['Technopoint'], 500)

    def test_calculate_avr_price_by_shop_list(self):
        product_list = [
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "A",
            },
            {
                "shop": "DNS",
                "product": 1,
                "price": 100,
                "series": "AB",
            },
            {
                "shop": "Technopoint",
                "product": 1,
                "price": 400,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 100,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 900,
                "series": "B",
            },
            {
                "shop": "DNS",
                "product": 2,
                "price": 100,
                "series": "AB",
            }
        ]
        result = calculate_avr_price_by_shop_list(product_list)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]['DNS'], 300)
        self.assertEqual(result[1]['Technopoint'], 400)
        self.assertEqual(result[2]['DNS'], 100)
        self.assertEqual(result[2]['Technopoint'], 500)

    def test_get_analog_list_of_product(self):
        original_product = {
            "shop": "DNS",
            "product": 1,
            "price": 500,
            "series": "A",
        }
        product_list = [
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "A",
            },
            {
                "shop": "DNS",
                "product": 1,
                "price": 100,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 2,
                "price": 400,
                "series": "A",
            }
        ]
        result = get_analog_list_of_product(original_product, product_list)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 2)

    def test_get_analog_list_of_product_list(self):
        product_list = [
            {
                "shop": "DNS",
                "product": 1,
                "price": 500,
                "series": "C",
            },
            {
                "shop": "DNS",
                "product": 1,
                "price": 100,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 3,
                "price": 400,
                "series": "B",
            },
            {
                "shop": "Technopoint",
                "product": 4,
                "price": 100,
                "series": "C",
            },
            {
                "shop": "Technopoint",
                "product": 5,
                "price": 900,
                "series": "C",
            }
        ]
        result = get_analog_list_of_product_list(product_list)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], [3])
        self.assertEqual(result[3], [1])
        self.assertEqual(result[4], [1, 5])
        self.assertEqual(result[5], [1, 4])

    def tearDown(self):
        pass
