from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api,reqparse, abort
from json import dumps
from flask_jsonpify import jsonify
from pymongo import MongoClient
import requests
import random
import json

app = Flask(__name__)
api = Api(app)

CORS(app)

mongo = MongoClient(
    'mongodb+srv://anol:anol@cluster0.1cvez.mongodb.net/techathon?retryWrites=true&w=majority')
db = mongo.get_database('techathon')

parser = reqparse.RequestParser()
parser.add_argument('data')

@app.route("/")
def hello():
    return jsonify("hello techathon")


class Products(Resource):
    def get(self):
        result= ""
        result1= ""
        array = []
        data = db.products.find({}, {'_id': 0})   
        for x in data:
            result = result +","+  str(x)
        result = result[1:]
        return jsonify(result)

class Product_name(Resource):
    def get(self,product_name):
        global ans
        result= ""
        result = db.products.find_one({'product_name':product_name},{'_id':0,'product_name':0,})
        ans = result.get("product_id")
        bid = random.randint(1,100)
        qty = random.randint(500,1000)
        payload = ( ('Pid', str(ans)),('Bid', str(bid)), ('Qnt', str(qty)))
        answer = requests.get("https://supplierevaluationrun.azurewebsites.net/predictRandomForest",params=payload)
        strfinaldict=answer.text
        finaldict = json.loads(strfinaldict) 
        ansdict = []
        for x in range(len(finaldict)):
            diction={"supplier":"","price":""}
            id = finaldict[x][0]
            price = finaldict[x][1]
            print(id)
            print(price)
            result = db.supplier.find_one({'supplier_id':id},{'_id':0,'supplier_id':0})
            name = result.get("supplier_name")
            diction["supplier"]=str(name)
            diction["price"]= price
            ansdict.append(diction)
        ansdict = sorted(ansdict, key = lambda i: i['price'])
        print(ansdict)
        return (ansdict) 

def callmodel(ans):
    print(type(ans))
    print(type(ans))
    y = ("api" + str(ans))
    return "cool"


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
        result = db.supplier.find_one({'supplier_id':supplier_id},{'_id':0,'supplier_id':0})
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

class Orders(Resource):
    def get(self):
        result= []
        result1= ""
        array = []
        data = db.previous_orders.find({}, {'_id': 0})   
        print(data)
        print(type(data))
        for x in data:
            result.append(x)
        return result

class Orders_id(Resource):
    def get(self,orders_id):
        print (orders_id)
        result= ""
        result = str(db.previous_orders.find_one({'order_no':orders_id},{'_id':0}))
        return jsonify(result) 



# api.add_resource(Job, '/job')
api.add_resource(Products, '/products')
api.add_resource(Product_name, '/products/<product_name>') # Route_3
api.add_resource(Suppliers, '/suppliers')
api.add_resource(Suppliers_id, '/suppliers/<supplier_id>')
api.add_resource(Buyers, '/buyers')
api.add_resource(Buyers_id, '/buyers/<buyer_id>')
api.add_resource(Orders, '/orders')
api.add_resource(Orders_id, '/orders/<orders_id>')

if __name__ == '__main__':
   app.run(port=5002)