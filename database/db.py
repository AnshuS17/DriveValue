import os
import csv
from datetime import datetime, timezone
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()

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
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            # Test connection
            self.client.admin.command('ping')
            
            # Extract database name from URI if provided, else use default DB_NAME
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
        csv_path = "data/raw/cars.csv"
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self._fallback_cars = []
                for idx, row in enumerate(reader):
                    row["_id"] = str(idx + 1)
                    row["year"] = int(row["year"])
                    row["price"] = int(float(row["price"]))
                    row["km_driven"] = int(float(row["km_driven"]))
                    row["engine_cc"] = int(float(row["engine_cc"]))
                    row["mileage"] = float(row["mileage"])
                    row["seats"] = int(float(row["seats"]))
                    row["insurance_valid"] = row["insurance_valid"].lower() in ["true", "1"]
                    self._fallback_cars.append(row)

    def get_stats(self):
        if self.is_connected:
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
        else:
            total_cars = len(self._fallback_cars)
            brands = len(set(c["brand"] for c in self._fallback_cars))
            avg_price = int(sum(c["price"] for c in self._fallback_cars) / total_cars) if total_cars else 0
            return {
                "total_cars": total_cars,
                "total_brands": brands,
                "avg_price": avg_price,
                "top_fuel_type": "Petrol",
                "db_status": "Offline (Using Local CSV)"
            }

    def get_cars(self, search="", brand="", fuel_type="", transmission="", year="", page=1, limit=12):
        if self.is_connected:
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
                
            return {"cars": cars, "total": total, "page": page, "pages": (total + limit - 1) // limit}
        else:
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
            return {"cars": paginated, "total": total, "page": page, "pages": (total + limit - 1) // limit}

    def get_car_by_id(self, car_id):
        if self.is_connected:
            from bson.objectid import ObjectId
            try:
                doc = self.cars_collection.find_one({"_id": ObjectId(car_id)})
                if doc:
                    doc["_id"] = str(doc["_id"])
                return doc
            except Exception:
                return None
        else:
            for c in self._fallback_cars:
                if str(c["_id"]) == str(car_id):
                    return c
            return None

    def add_car(self, car_data):
        if self.is_connected:
            result = self.cars_collection.insert_one(car_data)
            return str(result.inserted_id)
        else:
            car_data["_id"] = str(len(self._fallback_cars) + 1)
            self._fallback_cars.insert(0, car_data)
            return car_data["_id"]

    def delete_car(self, car_id):
        if self.is_connected:
            from bson.objectid import ObjectId
            try:
                res = self.cars_collection.delete_one({"_id": ObjectId(car_id)})
                return res.deleted_count > 0
            except Exception:
                return False
        else:
            initial = len(self._fallback_cars)
            self._fallback_cars = [c for c in self._fallback_cars if str(c["_id"]) != str(car_id)]
            return len(self._fallback_cars) < initial

    def get_similar_cars(self, brand, fuel_type, predicted_price, limit=4):
        if self.is_connected:
            # Query similar brand or fuel type within +/- 25% price range
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
                
            # If not enough matches, fallback to any brand
            if len(similar) < limit:
                cursor_fb = self.cars_collection.find({"price": {"$gte": min_p, "$lte": max_p}}).limit(limit)
                for doc in cursor_fb:
                    doc["_id"] = str(doc["_id"])
                    if doc not in similar:
                        similar.append(doc)
                    if len(similar) >= limit:
                        break
            return similar[:limit]
        else:
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
        if self.is_connected:
            try:
                self.predictions_collection.insert_one(doc)
            except Exception as e:
                print(f"Error saving prediction log: {e}")

db_manager = DatabaseManager()
