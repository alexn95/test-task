"""
Module contain django admin additional functionality
"""

from django.contrib import admin

from .tasks import get_cheap_products_chain, get_avg_prices_of_products_chain
from .tasks import get_analog_list_of_product_list_chain
from .forms import ProductDataAdminForm
from .models import ProductData


def cheap_products(modeladmin, request, queryset):
    """
    Admin activity for get cheap products from queryset
    :param queryset: products queryset
    :return:
    """
    id_list = list(map(lambda products: products.id, queryset))
    get_cheap_products_chain.delay(id_list)


cheap_products.short_description = "Get cheap products"


def avg_prices(modeladmin, request, queryset):
    """
    Admin activity for get average product prices from queryset
    :param queryset: products queryset
    :return:
    """
    id_list = list(map(lambda products: products.id, queryset))
    get_avg_prices_of_products_chain.delay(id_list)


avg_prices.short_description = "Get average prices of products"


def products_analogs(modeladmin, request, queryset):
    """
    Admin activity for get products analogs from queryset
    :param queryset: products queryset
    :return:
    """
    id_list = list(map(lambda products: products.id, queryset))
    get_analog_list_of_product_list_chain.delay(id_list)


products_analogs.short_description = "Get analogs of products"


class ProductDataAdmin(admin.ModelAdmin):
    """
    Product data model for admin
    """
    list_display = ('data_file', 'data_name', 'errors')
    actions = [cheap_products, avg_prices, products_analogs]
    form = ProductDataAdminForm


admin.site.register(ProductData, ProductDataAdmin)
