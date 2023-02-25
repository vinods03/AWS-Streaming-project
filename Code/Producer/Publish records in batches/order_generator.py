import random
import copy

from uuid import uuid4
from collections import namedtuple

customers = ['C101','C102','C103','C104','C105','C106','C107','C108','C109','C110']
sellers = ['S101','S102','S103','S104','S105']

product = namedtuple('product',['code','name','price'])
products = [
                 product('p101','abc',100),
                 product('p102','def',110),
                 product('p103','ghi',120),
                 product('p104','jkl',130),
                 product('p105','mno',140),
                 product('p106','pqr',150),
                 product('p107','stu',160),
                 product('p108','vwx',170),
                 product('p109','yza',180),
                 product('p110','bon',190),
               ]

def make_order():

    order_id = str(uuid4())
    customer_id = random.choice(customers)
    seller_id = random.choice(sellers)
    num_of_products_in_the_order = random.randint(1,len(products))
    rem_products = copy.copy(products)
    products_in_the_order = []

    for _ in range(num_of_products_in_the_order):
        product = random.choice(rem_products)
        products_in_the_order.append({'product_code': product.code, 'product_name': product.name, 'product_price': product.price, 'product_qty': random.randint(1,10)})
        rem_products.remove(product)

    order = {
        'order_id': order_id,
        'customer_id': customer_id,
        'seller_id': seller_id,
        'products': products_in_the_order
    }

    return order