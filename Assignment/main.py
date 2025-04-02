from itertools import product
from fastapi import FastAPI
import json
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import requests
import os
from pydantic import BaseModel

app = FastAPI()    
@app.get("/getSingleProduct/{item_id}")
def get_single_product(item_id: str):
    MONGO_URI = "mongodb+srv://root2:root2@cluster10.kk12w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(MONGO_URI)
    db = client.WebService
    collection = db.Col
    print("item id is " + str(item_id))
    print(item_id)
    results = dumps(collection.find_one({"Product ID": item_id}))
    return json.loads(results)

@app.get("/getAll")
def get_all_products():
    MONGO_URI = "mongodb+srv://root2:root2@cluster10.kk12w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(MONGO_URI)
    db = client.WebService
    collection = db.Col
    results = dumps(collection.find())
    return json.loads(results)  
  
@app.get("/addNew/{item_id}")
def add_new_product(item_id: str):
    MONGO_URI = "mongodb+srv://root2:root2@cluster10.kk12w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(MONGO_URI)
    db = client.WebService
    collection = db.Col
    newRecord= {"Product Id": 101, "Name": "starter", "UnitPrice": 200, "StockQuantity": 30, "Description": "High-quality Starter"}	
    newRecord= {"Product Id": 102, "Name": "start", "UnitPrice": 300, "StockQuantity": 40, "Description": "High-quality Start"}
    res = collection.insert_one(newRecord)
    return {"status":"inserted"}


@app.get("/deleteOne/{item_id}")
def add_new_product(item_id: str):
    MONGO_URI = "mongodb+srv://root2:root2@cluster10.kk12w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(MONGO_URI)
    db = client.WebService
    collection = db.Col
    deleteRecord= {"Product Id": 101, "Name": "starter", "UnitPrice": 200, "StockQuantity": 30, "Description": "High-quality Starter"}	
    res = collection.delete_one(deleteRecord)
    return {"status":"deleted"}

@app.get("/startWith/{letter}")
def get_products_starting_with(letter: str):
    MONGO_URI = "mongodb+srv://root2:root2@cluster10.kk12w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(MONGO_URI)
    db = client.WebService
    collection = db.Col
    return json.loads(dumps(collection.find({"name": {"$regex": letter, "$options": "i"}})))

@app.get("/convert/{item_id}")
def convert_price_to_eur(item_id: str):
    MONGO_URI = "mongodb+srv://root2:root2@cluster10.kk12w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(MONGO_URI)
    db = client.WebService
    collection = db.Col
    product = collection.find_one({"Product ID": item_id})
    unit_price = product.get("Unit Price")
    url = 'https://currency-converter5.p.rapidapi.com/currency/convert?format=json&from=USD&to=EUR&amount=1&language=en'
    headers = {
        'x-rapidapi-key': '65a84db33cmshf211b6817ea17d8p191775jsn3b3820a40528',
		'x-rapidapi-host': 'currency-converter5.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)
    exchange_data = response.json()
    exchange_rate = exchange_data.get('response', {}).get('conversion_rate')
    if not exchange_rate:
        return {"error": "EUR conversion rate not available"}
    eur_price = unit_price * exchange_rate
    return {"product_id": item_id, "usd_price": unit_price, "eur_price": eur_price}

