import json


def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_products(cate_id=None, kw=None, from_price=None, to_price=None):
    products = read_data(path='data/products.json')

    if cate_id:
        cate_id = int(cate_id)
        products = [p for p in products \
                    if p['category_id'] == cate_id]

    if kw:
        products = [p for p in products \
                    if p['name'].find(kw) >= 0]

    if from_price and to_price:
        from_price = float(from_price)
        to_price = float(to_price)
        products = [p for p in products \
                    if to_price >= p['price'] >= from_price]

    return products


def get_product_by_id(product_id):
    products = read_data(path='data/products.json')
    for p in products:
        if p["id"] == product_id:
            return p
