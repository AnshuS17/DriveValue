import os
import csv
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/auto_value_ai")
DB_NAME = "auto_value_ai"

def seed_database(filepath="data/raw/cars.csv"):
    """
    Reads dataset from CSV and seeds into MongoDB collection.
    """
    if not os.path.exists(filepath):
        print(f"Error: Dataset file '{filepath}' not found.")
        return False

    print(f"Connecting to MongoDB at {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        # Verify connection
        client.admin.command('ping')
        
        db = client[DB_NAME]
        cars_col = db["cars"]
        
        print("Clearing existing records in 'cars' collection...")
        cars_col.delete_many({})
        
        records = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = {
                    "brand": row["brand"],
                    "model": row["model"],
                    "variant": row["variant"],
                    "year": int(row["year"]),
                    "fuel_type": row["fuel_type"],
                    "transmission": row["transmission"],
                    "km_driven": int(float(row["km_driven"])),
                    "engine_cc": int(float(row["engine_cc"])),
                    "mileage": float(row["mileage"]),
                    "ownership": row["ownership"],
                    "location": row["location"],
                    "seats": int(float(row["seats"])),
                    "condition": row["condition"],
                    "insurance_valid": row["insurance_valid"].lower() in ["true", "1"],
                    "price": int(float(row["price"]))
                }
                records.append(record)
                
        print(f"Inserting {len(records)} records into MongoDB...")
        if records:
            cars_col.insert_many(records)
            
        print("Creating MongoDB indexes for fast search and filtering...")
        cars_col.create_index([("brand", 1), ("model", 1)])
        cars_col.create_index([("fuel_type", 1)])
        cars_col.create_index([("transmission", 1)])
        cars_col.create_index([("price", 1)])
        cars_col.create_index([("$**", "text")])
        
        print("--> Database Seeding Complete Successfully!")
        return True
    except Exception as e:
        print(f"--> Seeding Error: {e}")
        print("Please ensure MongoDB is running or check your MONGO_URI in .env")
        return False

if __name__ == "__main__":
    seed_database()
