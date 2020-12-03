from flask import render_template, request, session, jsonify, redirect
from saleapp import app, utils, login
from saleapp.admin import *
from flask_login import login_user
import os, json
from saleapp import decorator


@app.route("/")
def index():
    categories = utils.read_data()
    return render_template('index.html',
                           categories=categories)


@app.route("/products")
def product_list():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    products = utils.read_products(cate_id=cate_id,
                                   kw=kw,
                                   from_price=from_price,
                                   to_price=to_price)

    return render_template('product-list.html',
                           products=products)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id=product_id)

    return render_template('product-detail.html',
                           product=product)


@app.route('/login', methods=['post'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        if password == confirm:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            f = request.files["avatar"]
            avatar_path = 'images/upload/%s' % f.filename
            f.save(os.path.join(app.root_path, 'static/', avatar_path))
            if utils.register_user(name=name, username=username, password=password,
                                   email=email, avatar=avatar_path):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang bị lỗi! Vui lòng thực hiện sau!"
        else:
            err_msg = "Mật khâu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("price", 0)

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    quantity, amount = utils.cart_stats(cart)

    return jsonify({
        "total_quantity": quantity,
        "total_amount": amount
    })


@app.route('/payment')
def payment():
    quantity, amount = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_quantity": quantity,
        "total_amount": amount
    }
    return render_template('payment.html', cart_info=cart_info)


@app.route('/api/pay', methods=['post'])
@decorator.login_required
def pay():
    if utils.add_receipt(session.get('cart')):
        del session['cart']

        return jsonify({
            "message": "Add receipt successful!",
            "err_code": 200
        })

    return jsonify({
        "message": "Failed"
    })


@login.user_loader
def get_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
