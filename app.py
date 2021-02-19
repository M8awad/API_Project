from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


#Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#dataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init dp
db = SQLAlchemy(app)

#Init marshmallow
ma = Marshmallow(app)


#product class

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        
#product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')
      
        
#init schema_schema 
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=true, strict=True)
                
#create product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    
    new_product = product(name,description,price,qty)
    
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product)

#get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

#get product by id
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = product.query.get(id)
    return product_schema.jsonify(product)

#update the current products
@app.route('product/<id>', methods=['PUT'])
def update_product(id):
    product = product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    
    db.session.commit()
    return product_schema.jsonify(product)

#delet a product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)
    


#run server
if __name__ == '__main__':
    app.run(debug=True)