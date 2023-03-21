from flask import Blueprint, render_template
from models import Product

blp = Blueprint('main', __name__)

@blp.get('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products = products)

@blp.get('/contacto')
def contact():
    return render_template('contact.html')
