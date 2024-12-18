from product.models import Product, Order, OrderProduct

from django.db.models import Sum

from shared.models import ACIAdmin

from datetime import datetime

from collections.abc import Iterable

SQL_FOR_ORDER_TRANSACTION_PRICE = """
    SELECT o.*, SUM(op.total_price) FROM transaction_order o
    inner join order_product op on o.id = op.order_id
    group by o.id
    having SUM(op.total_price) <= %s;
"""



def find_total_sells_for_product(order_products):
    order_products = order_products.annotate(total_sum=Sum("total_price"))
    return order_products.first().total_price


def check_if_user_is_admin(request):
    if not request.user.is_anonymous:
        return ACIAdmin.objects.filter(user=request.user).exists()
    return False

def get_the_last_part_of_date_key(key):
    if isinstance(key, str) and key:
        return key[-3:]
    return ''

def parse_string_to_date(data):
    if isinstance(data, str):
        return datetime.strptime(data, '%Y-%m-%d')
    return ''

def get_keys_that_contains_date(keys):
    if hasattr(keys, '__iter__'):
        return [element for element in keys if 'date' in element]
    return []



