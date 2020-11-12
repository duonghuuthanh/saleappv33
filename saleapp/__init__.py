from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)
app.secret_key = '^%*&!^@^*gsuias1&^&!*^!&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/saledbv1?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="IT82 SHOP", template_mode='bootstrap4')