# MongoClient Import
from pymongo import MongoClient

MONGODB_URL = "mongodb://localhost:27017"
client = MongoClient(MONGODB_URL)

db = client.backend_db
books_collection = db.books
users_collection = db.users

