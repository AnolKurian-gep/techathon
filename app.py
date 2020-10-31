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
    def get(self,product_name):
        print (product_name)
        result= ""
        result = str(db.categories.find_one({'product':product_name},{'_id':0}))
        return jsonify(result) 

api.add_resource(Products, '/products')
api.add_resource(Categories, '/products/<product_name>') # Route_3

if __name__ == '__main__':
   app.run(port=5002)