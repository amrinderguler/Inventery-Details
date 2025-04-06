from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB

def get_db_connection():
    """Establish connection to MongoDB"""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db

def save_server_data(data):
    """Save server data to MongoDB using serial number as primary key"""
    db = get_db_connection()
    
    serial_number = data.get("serial_number")
    if not serial_number:
        raise ValueError("Serial number not found in server data")
    
    # Use serial number as primary key (_id)
    data["_id"] = serial_number
    
    # Update document if exists, insert otherwise (upsert)
    result = db.servers.update_one(
        {"_id": serial_number},
        {"$set": data},
        upsert=True
    )
    
    return result
