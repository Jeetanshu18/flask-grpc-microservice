import pymongo

# Define your database connection settings here
MONGO_URI = "mongodb"
MONGO_DB = "flask_microservice"

# Initialize the MongoDB client
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]

# Optionally, you can define functions or classes here for more advanced setup
# For example, you can define a function to return a collection object:
# def get_user_collection():
#     return db['users']
