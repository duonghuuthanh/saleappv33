from flask import render_template
from saleapp import app, utils


@app.route("/")
def index():
    categories = utils.read_data()
    return render_template('index.html',
                           categories=categories)


@app.route("/products")
def product_list():
    products = utils.read_data(path='data/products.json')

    return render_template('product-list.html', products=products)


if __name__ == "__main__":
    app.run(debug=True)
