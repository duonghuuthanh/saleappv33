import json, hashlib
from saleapp.models import User, UserRole, Product
from saleapp import db


def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_products(cate_id=None, kw=None, from_price=None, to_price=None):
    products = Product.query

    if cate_id:
        products = products.filter(Product.catgory_id == cate_id)

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price and to_price:
        products = products.filter(Product.price.__gt__(from_price),
                                   Product.price.__lt__(to_price))

    return products.all()
    # products = read_data(path='data/products.json')
    #
    # if cate_id:
    #     cate_id = int(cate_id)
    #     products = [p for p in products \
    #                 if p['category_id'] == cate_id]
    #
    # if kw:
    #     products = [p for p in products \
    #                 if p['name'].find(kw) >= 0]
    #
    # if from_price and to_price:
    #     from_price = float(from_price)
    #     to_price = float(to_price)
    #     products = [p for p in products \
    #                 if to_price >= p['price'] >= from_price]
    #
    # return products


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # products = read_data(path='data/products.json')
    # for p in products:
    #     if p["id"] == product_id:
    #         return p


def check_login(username, password, role=UserRole.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.user_role == role).first()

    return user


def get_user_by_id(user_id):
    return User.query.get(user_id)


def register_user(name, email, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             username=username,
             password=password,
             avatar=avatar,
             user_role=UserRole.USER)
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except:
        return False


def cart_stats(cart):
    total_amount, total_quantity = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"]*p["price"]

    return total_quantity, total_amount