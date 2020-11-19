import json, hashlib
from saleapp.models import User, UserRole


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


def check_login(username, password, role=UserRole.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.user_role == role).first()

    return user

def get_user_by_id(user_id):
    return User.query.get(user_id)
