import os
import csv
from datetime import datetime, timezone
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/auto_value_ai")
DB_NAME = "auto_value_ai"

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.cars_collection = None
        self.predictions_collection = None
        self.is_connected = False
        self._fallback_cars = []
        
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=800)
            self.client.admin.command('ping')
            
            db_name = DB_NAME
            if "/" in MONGO_URI.replace("mongodb://", "").replace("mongodb+srv://", ""):
                uri_db = MONGO_URI.split("/")[-1].split("?")[0]
                if uri_db:
                    db_name = uri_db
                    
            self.db = self.client[db_name]
            self.cars_collection = self.db["cars"]
            self.predictions_collection = self.db["predictions"]
            self.is_connected = True
            print(f"--> Successfully connected to MongoDB ({db_name})")
        except Exception as e:
            self.is_connected = False
            print(f"--> MongoDB Connection Warning: {e}")
            print("--> Falling back to CSV dataset in-memory cache for seamless execution.")
            self._load_fallback_cars()

    def _load_fallback_cars(self):
        csv_path = os.path.join(BASE_DIR, "data", "raw", "cars.csv")
        self._fallback_cars = []
        if os.path.exists(csv_path):
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for idx, row in enumerate(reader):
                        try:
                            record = {
                                "_id": str(idx + 1),
                                "brand": str(row.get("brand", "Toyota")),
                                "model": str(row.get("model", "Fortuner")),
                                "variant": str(row.get("variant", "Standard")),
                                "year": int(row.get("year", 2021)),
                                "price": int(float(row.get("price", 850000))),
                                "km_driven": int(float(row.get("km_driven", 45000))),
                                "fuel_type": str(row.get("fuel_type", "Diesel")),
                                "transmission": str(row.get("transmission", "Automatic")),
                                "engine_cc": int(float(row.get("engine_cc", 1197))),
                                "mileage": float(row.get("mileage", 18.0)),
                                "ownership": str(row.get("ownership", "1st Owner")),
                                "location": str(row.get("location", "Mumbai")),
                                "seats": int(float(row.get("seats", 5))),
                                "condition": str(row.get("condition", "Good")),
                                "insurance_valid": str(row.get("insurance_valid", "true")).lower() in ["true", "1"]
                            }
                            self._fallback_cars.append(record)
                        except Exception:
                            continue
            except Exception as e:
                print(f"Error loading CSV fallback dataset: {e}")

    def get_stats(self):
        if self.is_connected and self.cars_collection:
            try:
                total_cars = self.cars_collection.count_documents({})
                brands = len(self.cars_collection.distinct("brand"))
                
                pipeline = [{"$group": {"_id": None, "avg_price": {"$avg": "$price"}}}]
                avg_result = list(self.cars_collection.aggregate(pipeline))
                avg_price = int(avg_result[0]["avg_price"]) if avg_result else 0
                
                fuel_pipeline = [
                    {"$group": {"_id": "$fuel_type", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 1}
                ]
                fuel_result = list(self.cars_collection.aggregate(fuel_pipeline))
                top_fuel = fuel_result[0]["_id"] if fuel_result else "N/A"
                
                return {
                    "total_cars": total_cars,
                    "total_brands": brands,
                    "avg_price": avg_price,
                    "top_fuel_type": top_fuel,
                    "db_status": "Connected to MongoDB"
                }
            except Exception as e:
                print(f"Error executing Mongo stats query: {e}")
                
        total_cars = len(self._fallback_cars)
        brands = len(set(c["brand"] for c in self._fallback_cars)) if total_cars > 0 else 17
        avg_price = int(sum(c["price"] for c in self._fallback_cars) / total_cars) if total_cars > 0 else 850000
        return {
            "total_cars": total_cars or 2750,
            "total_brands": brands,
            "avg_price": avg_price,
            "top_fuel_type": "Petrol",
            "db_status": "Offline (Using Local CSV)"
        }

    def get_cars(self, search="", brand="", fuel_type="", transmission="", year="", page=1, limit=12):
        if self.is_connected and self.cars_collection:
            try:
                query = {}
                if search:
                    query["$or"] = [
                        {"brand": {"$regex": search, "$options": "i"}},
                        {"model": {"$regex": search, "$options": "i"}},
                        {"variant": {"$regex": search, "$options": "i"}},
                        {"location": {"$regex": search, "$options": "i"}}
                    ]
                if brand:
                    query["brand"] = brand
                if fuel_type:
                    query["fuel_type"] = fuel_type
                if transmission:
                    query["transmission"] = transmission
                if year:
                    try:
                        query["year"] = int(year)
                    except ValueError:
                        pass

                total = self.cars_collection.count_documents(query)
                skip = (page - 1) * limit
                cursor = self.cars_collection.find(query).skip(skip).limit(limit)
                
                cars = []
                for doc in cursor:
                    doc["_id"] = str(doc["_id"])
                    cars.append(doc)
                    
                return {"cars": cars, "total": total, "page": page, "pages": max(1, (total + limit - 1) // limit)}
            except Exception as e:
                print(f"Error querying Mongo cars: {e}")

        filtered = self._fallback_cars
        if search:
            s = search.lower()
            filtered = [c for c in filtered if s in c["brand"].lower() or s in c["model"].lower() or s in c["variant"].lower() or s in c["location"].lower()]
        if brand:
            filtered = [c for c in filtered if c["brand"] == brand]
        if fuel_type:
            filtered = [c for c in filtered if c["fuel_type"] == fuel_type]
        if transmission:
            filtered = [c for c in filtered if c["transmission"] == transmission]
        if year:
            try:
                y = int(year)
                filtered = [c for c in filtered if c["year"] == y]
            except ValueError:
                pass

        total = len(filtered)
        skip = (page - 1) * limit
        paginated = filtered[skip:skip+limit]
        return {"cars": paginated, "total": total, "page": page, "pages": max(1, (total + limit - 1) // limit)}

    def get_car_by_id(self, car_id):
        if self.is_connected and self.cars_collection:
            from bson.objectid import ObjectId
            try:
                doc = self.cars_collection.find_one({"_id": ObjectId(car_id)})
                if doc:
                    doc["_id"] = str(doc["_id"])
                return doc
            except Exception:
                pass
                
        for c in self._fallback_cars:
            if str(c["_id"]) == str(car_id):
                return c
        return None

    def add_car(self, car_data):
        if self.is_connected and self.cars_collection:
            try:
                result = self.cars_collection.insert_one(car_data)
                return str(result.inserted_id)
            except Exception as e:
                print(f"Error inserting car to Mongo: {e}")
                
        car_data["_id"] = str(len(self._fallback_cars) + 1)
        self._fallback_cars.insert(0, car_data)
        return car_data["_id"]

    def delete_car(self, car_id):
        if self.is_connected and self.cars_collection:
            from bson.objectid import ObjectId
            try:
                res = self.cars_collection.delete_one({"_id": ObjectId(car_id)})
                return res.deleted_count > 0
            except Exception:
                pass

        initial = len(self._fallback_cars)
        self._fallback_cars = [c for c in self._fallback_cars if str(c["_id"]) != str(car_id)]
        return len(self._fallback_cars) < initial

    def get_similar_cars(self, brand, fuel_type, predicted_price, limit=4):
        if self.is_connected and self.cars_collection:
            try:
                min_p = predicted_price * 0.75
                max_p = predicted_price * 1.25
                query = {
                    "$or": [{"brand": brand}, {"fuel_type": fuel_type}],
                    "price": {"$gte": min_p, "$lte": max_p}
                }
                cursor = self.cars_collection.find(query).limit(limit)
                similar = []
                for doc in cursor:
                    doc["_id"] = str(doc["_id"])
                    similar.append(doc)
                    
                if len(similar) < limit:
                    cursor_fb = self.cars_collection.find({"price": {"$gte": min_p, "$lte": max_p}}).limit(limit)
                    for doc in cursor_fb:
                        doc["_id"] = str(doc["_id"])
                        if doc not in similar:
                            similar.append(doc)
                        if len(similar) >= limit:
                            break
                return similar[:limit]
            except Exception as e:
                print(f"Error fetching Mongo similar cars: {e}")

        min_p = predicted_price * 0.75
        max_p = predicted_price * 1.25
        matches = [c for c in self._fallback_cars if (c["brand"] == brand or c["fuel_type"] == fuel_type) and min_p <= c["price"] <= max_p]
        if len(matches) < limit:
            matches += [c for c in self._fallback_cars if min_p <= c["price"] <= max_p and c not in matches]
        return matches[:limit]

    def save_prediction(self, input_data, predicted_price):
        doc = {
            "input_data": input_data,
            "predicted_price": predicted_price,
            "created_at": datetime.now(timezone.utc)
        }
        if self.is_connected and self.predictions_collection:
            try:
                self.predictions_collection.insert_one(doc)
            except Exception as e:
                print(f"Error saving prediction log: {e}")

db_manager = DatabaseManager()
