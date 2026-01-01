from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# MongoDB Connection
""" client = MongoClient("mongodb://localhost:27017/")
db = client["MentalHealth"]
users_collection = db["users"] """

# Utility: Create User
def create_user(users_collection, user_data):
    user_data["topic"]=None
    user_data["createdAt"] = datetime.utcnow()
    user_data["updatedAt"] = datetime.utcnow()
    result = users_collection.insert_one(user_data)
    return result.inserted_id

# Utility: Find User by Email
def find_by_email(users_collection, email):
    return users_collection.find_one({"email": email})
    

# Utility: Update User Password
def update_password(users_collection, user_id, new_hashed_password):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "password": new_hashed_password,
            "updatedAt": datetime.utcnow()
        }}
    )
    return True

