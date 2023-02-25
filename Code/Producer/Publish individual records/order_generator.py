import random
import copy
from uuid import uuid4
from collections import namedtuple

customer_ids = ['c100','c101','c102','c103','c104','c105','c106','c107','c108','c109','c110']
seller_ids = ['s100','s101','s102','s103','s104','s105','s106','s107','s108','s109','s110']
product = namedtuple('product',['code','name','price']) 
products = [
            product('p101','abc',100),
            product('p102','def',110),
            product('p103','geh',120),
            product('p104','ijk',130),
            product('p105','lmn',140),
            product('p106','opq',150),
            product('p107','rst',160),
            product('p108','uvw',170),
            product('p109','xyz',180),
            product('p110','amp',190)
          ]


def make_order():

    order_id = str(uuid4())
    customer_id = random.choice(customer_ids)
    seller_id = random.choice(seller_ids)

    num_of_products_in_order = random.randint(1, len(products))
    products_not_yet_included_in_order = copy.copy(products)
    products_in_order = []

    for _ in range(num_of_products_in_order):
        product = random.choice(products_not_yet_included_in_order)
        products_not_yet_included_in_order.remove(product)
        products_in_order.append({'product_code': product.code, 'product_name': product.name, 'product_price': product.price, 'product_qty': random.randint(1,10)})

    final_order = {
        'order_id': order_id,
        'customer_id': customer_id,
        'seller_id': seller_id,
        'products': products_in_order
    }

    return final_order