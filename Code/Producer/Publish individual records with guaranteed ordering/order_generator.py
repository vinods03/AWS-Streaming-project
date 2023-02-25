import random
import copy
from uuid import uuid4
from collections import namedtuple

customers = ['C101','C102','C103','C104','C105','C106','C107','C108','C109','C110']
sellers = ['S101','S102','S103','S104']
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
             product('p109','yzq',180),
             product('p110','bon',190),
]

def make_order():

    order_id = str(uuid4())
    customer_id = random.choice(customers)
    seller_id = random.choice(sellers)
    
    num_products_in_order = random.randint(1,len(products))
    remaining_products = copy.copy(products)
    products_in_order = []

    for _ in range(1, num_products_in_order):
        product = random.choice(remaining_products)
        remaining_products.remove(product)
        products_in_order.append(product)


    final_order = {
        'order_id': order_id,
        'customer_id': customer_id,
        'seller_id': seller_id,
        'products': products_in_order
    }

    return final_order