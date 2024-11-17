from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import *
import requests
import json

client = MongoClient('localhost', 27017)
db = client['books'] # создаем базу данных
collection = db['info'] # создаем коллекцию

collection.delete_many({})

with open('books.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Вставка данных в коллекцию
if isinstance(data, list):
    collection.insert_many(data)  # Если данные - это список
else:
    collection.insert_one(data)    # Если данные - это один объект

print("Данные успешно загружены в MongoDB")

count = 0

for index, doc in enumerate(collection.find({'description': {'$regex': 'love', '$options': 'i'}}, {'_id': 0}),1):
    count += 1
    print(f"{index}.", doc)
print(f"Количество книг про любовь: {count}")

for index, doc in enumerate(collection.find({'price': {'$gt': 50.0, '$lt': 55.0}, 
                      'stock': {'$gt': 10}}), 1):
    count += 1
    print(f"{index}. {doc['name']}")
print(f"Количество книг по запросу: {count}")

for doc in collection.find({"$or": [{'price': {'$lt': 20.0}}, {'stock': 1}]}):
    print(f"Название: {doc['name']}, Цена: {doc['price']}, Остаток: {doc['stock']}")

