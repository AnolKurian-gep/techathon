from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)

CORS(app)

mongo = MongoClient(
    'mongodb+srv://anol:anol@cluster0.1cvez.mongodb.net/techathon?retryWrites=true&w=majority')
db = mongo.get_database('techathon')

@app.route("/")
def hello():
    return jsonify("hello techathon")

class Products(Resource):
    def get(self):
        result= ""
        result1= ""
        array = []
        data = db.categories.find({}, {'_id': 0})   
        for x in data:
            result = result +","+  str(x)
        result = result[1:]
        return jsonify(result)

class Categories(Resource):
    def get(self,product_id):
        print (product_id)
        result= ""
        result = str(db.categories.find_one({'product_id':product_id},{'_id':0,'supplier_id':0}))
        return jsonify(result) 

class Suppliers(Resource):
    def get(self):
        result= ""
        array = []
        data = db.supplier.find({}, {'_id': 0})   
        for x in data:
            result = result +","+  str(x)
        result = result[1:]
        return jsonify(result)

class Suppliers_id(Resource):
    def get(self,supplier_id):
        print (supplier_id)
        result= ""
        result = str(db.supplier.find_one({'supplier_id':supplier_id},{'_id':0}))
        return jsonify(result) 

class Buyers(Resource):
    def get(self):
        result= ""
        result1= ""
        array = []
        data = db.buyer.find({}, {'_id': 0})   
        for x in data:
            result = result +","+  str(x)
        result = result[1:]
        return jsonify(result)

class Buyers_id(Resource):
    def get(self,buyer_id):
        print (buyer_id)
        result= ""
        result = str(db.buyer.find_one({'buyer_id':buyer_id},{'_id':0}))
        return jsonify(result) 


api.add_resource(Products, '/products')
api.add_resource(Categories, '/products/<product_id>') # Route_3
api.add_resource(Suppliers, '/suppliers')
api.add_resource(Suppliers_id, '/suppliers/<supplier_id>')
api.add_resource(Buyers, '/buyers')
api.add_resource(Buyers_id, '/buyers/<buyer_id>')

if __name__ == '__main__':
   app.run(port=5002)