import os
import csv
import random

# Set random seed for reproducible dataset generation
random.seed(42)

# Directory setup
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# Brand, Model, Variants, and specs mapping
CAR_CATALOG = {
    "Maruti Suzuki": {
        "Swift": {"variants": ["LXi", "VXi", "ZXi", "ZXi Plus"], "base_price": 650000, "engine": 1197, "mileage": 22.3, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Baleno": {"variants": ["Sigma", "Delta", "Zeta", "Alpha"], "base_price": 720000, "engine": 1197, "mileage": 22.9, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Brezza": {"variants": ["LXi", "VXi", "ZXi", "ZXi Plus"], "base_price": 950000, "engine": 1462, "mileage": 19.8, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Dzire": {"variants": ["LXi", "VXi", "ZXi", "ZXi Plus"], "base_price": 700000, "engine": 1197, "mileage": 24.1, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Ertiga": {"variants": ["LXi", "VXi", "ZXi", "ZXi Plus"], "base_price": 980000, "engine": 1462, "mileage": 20.5, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "Wagon R": {"variants": ["LXi", "VXi", "ZXi"], "base_price": 580000, "engine": 998, "mileage": 25.2, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Alto": {"variants": ["Std", "LXi", "VXi"], "base_price": 390000, "engine": 796, "mileage": 24.7, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual"], "seats": 5},
        "Grand Vitara": {"variants": ["Sigma", "Delta", "Zeta", "Alpha"], "base_price": 1250000, "engine": 1490, "mileage": 27.9, "fuels": ["Petrol", "Hybrid"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Ciaz": {"variants": ["Sigma", "Delta", "Zeta", "Alpha"], "base_price": 950000, "engine": 1462, "mileage": 20.0, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5}
    },
    "Hyundai": {
        "Creta": {"variants": ["E", "EX", "S", "SX", "SX(O)"], "base_price": 1200000, "engine": 1497, "mileage": 16.8, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "i20": {"variants": ["Magna", "Sportz", "Asta", "Asta(O)"], "base_price": 780000, "engine": 1197, "mileage": 20.35, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Verna": {"variants": ["EX", "S+", "SX", "SX(O)"], "base_price": 1150000, "engine": 1497, "mileage": 18.6, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Venue": {"variants": ["E", "S", "S+", "SX", "SX(O)"], "base_price": 880000, "engine": 1197, "mileage": 17.5, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Grand i10 Nios": {"variants": ["Era", "Magna", "Sportz", "Asta"], "base_price": 620000, "engine": 1197, "mileage": 20.7, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Alcazar": {"variants": ["Prestige", "Platinum", "Signature"], "base_price": 1680000, "engine": 1493, "mileage": 18.1, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7}
    },
    "Tata": {
        "Nexon": {"variants": ["Smart", "Pure", "Creative", "Fearless"], "base_price": 900000, "engine": 1199, "mileage": 17.4, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Punch": {"variants": ["Pure", "Adventure", "Accomplished", "Creative"], "base_price": 680000, "engine": 1199, "mileage": 20.0, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Harrier": {"variants": ["Smart", "Pure", "Adventure", "Fearless"], "base_price": 1750000, "engine": 1956, "mileage": 16.8, "fuels": ["Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Safari": {"variants": ["Smart", "Pure", "Adventure", "Accomplished"], "base_price": 1880000, "engine": 1956, "mileage": 16.3, "fuels": ["Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "Altroz": {"variants": ["XE", "XM", "XT", "XZ", "XZ+"], "base_price": 720000, "engine": 1199, "mileage": 19.3, "fuels": ["Petrol", "Diesel", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Tiago": {"variants": ["XE", "XM", "XT", "XZ+"], "base_price": 580000, "engine": 1199, "mileage": 20.0, "fuels": ["Petrol", "CNG", "Electric"], "transmissions": ["Manual", "Automatic"], "seats": 5}
    },
    "Honda": {
        "City": {"variants": ["V", "VX", "ZX"], "base_price": 1280000, "engine": 1498, "mileage": 17.8, "fuels": ["Petrol", "Hybrid"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Amaze": {"variants": ["E", "S", "VX"], "base_price": 750000, "engine": 1199, "mileage": 18.6, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "WR-V": {"variants": ["SV", "VX"], "base_price": 920000, "engine": 1498, "mileage": 17.5, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual"], "seats": 5},
        "Civic": {"variants": ["V", "VX", "ZX"], "base_price": 1850000, "engine": 1799, "mileage": 16.5, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5}
    },
    "Toyota": {
        "Fortuner": {"variants": ["2.7 4x2", "2.8 4x2 AT", "2.8 4x4 AT", "Legender"], "base_price": 3500000, "engine": 2755, "mileage": 14.2, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "Innova Crysta": {"variants": ["GX", "VX", "ZX"], "base_price": 2100000, "engine": 2393, "mileage": 15.1, "fuels": ["Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "Glanza": {"variants": ["E", "S", "G", "V"], "base_price": 750000, "engine": 1197, "mileage": 22.3, "fuels": ["Petrol", "CNG"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Camry": {"variants": ["2.5 Hybrid"], "base_price": 4600000, "engine": 2487, "mileage": 19.1, "fuels": ["Hybrid"], "transmissions": ["Automatic"], "seats": 5}
    },
    "Mahindra": {
        "Thar": {"variants": ["AX(O)", "LX Petrol AT", "LX Diesel AT"], "base_price": 1400000, "engine": 2184, "mileage": 15.2, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 4},
        "XUV700": {"variants": ["MX", "AX3", "AX5", "AX7", "AX7L"], "base_price": 1650000, "engine": 2184, "mileage": 14.0, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "Scorpio-N": {"variants": ["Z2", "Z4", "Z6", "Z8", "Z8L"], "base_price": 1550000, "engine": 2184, "mileage": 14.5, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "XUV300": {"variants": ["W4", "W6", "W8", "W8(O)"], "base_price": 890000, "engine": 1497, "mileage": 20.0, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Bolero": {"variants": ["B4", "B6", "B6(O)"], "base_price": 980000, "engine": 1493, "mileage": 16.0, "fuels": ["Diesel"], "transmissions": ["Manual"], "seats": 7}
    },
    "Kia": {
        "Seltos": {"variants": ["HTE", "HTK", "HTX", "GTX+", "X-Line"], "base_price": 1250000, "engine": 1497, "mileage": 17.0, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Sonet": {"variants": ["HTE", "HTK", "HTX", "GTX+"], "base_price": 850000, "engine": 1197, "mileage": 18.4, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Carens": {"variants": ["Premium", "Prestige", "Luxury", "Luxury Plus"], "base_price": 1180000, "engine": 1497, "mileage": 16.5, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 7}
    },
    "Volkswagen": {
        "Virtus": {"variants": ["Comfortline", "Highline", "Topline", "GT Plus"], "base_price": 1220000, "engine": 1498, "mileage": 18.6, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Taigun": {"variants": ["Comfortline", "Highline", "Topline", "GT"], "base_price": 1280000, "engine": 1498, "mileage": 17.8, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Polo": {"variants": ["Trendline", "Comfortline", "Highline", "GT TSI"], "base_price": 680000, "engine": 999, "mileage": 18.2, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5}
    },
    "Skoda": {
        "Slavia": {"variants": ["Active", "Ambition", "Style"], "base_price": 1200000, "engine": 1498, "mileage": 18.5, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Kushaq": {"variants": ["Active", "Ambition", "Style", "Monte Carlo"], "base_price": 1260000, "engine": 1498, "mileage": 17.9, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Octavia": {"variants": ["Style", "L&K"], "base_price": 2800000, "engine": 1984, "mileage": 15.8, "fuels": ["Petrol"], "transmissions": ["Automatic"], "seats": 5}
    },
    "Renault": {
        "Kwid": {"variants": ["RXT", "CLIMBER"], "base_price": 500000, "engine": 999, "mileage": 22.0, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Triber": {"variants": ["RXE", "LXL", "RXT", "RXZ"], "base_price": 680000, "engine": 999, "mileage": 19.0, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 7},
        "Kiger": {"variants": ["RXE", "RXT", "RXZ"], "base_price": 720000, "engine": 999, "mileage": 19.1, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5}
    },
    "MG": {
        "Hector": {"variants": ["Style", "Shine", "Smart", "Sharp Pro"], "base_price": 1550000, "engine": 1956, "mileage": 15.8, "fuels": ["Petrol", "Diesel"], "transmissions": ["Manual", "Automatic"], "seats": 5},
        "Astor": {"variants": ["Style", "Super", "Smart", "Sharp"], "base_price": 1100000, "engine": 1498, "mileage": 14.8, "fuels": ["Petrol"], "transmissions": ["Manual", "Automatic"], "seats": 5}
    },
    "BMW": {
        "3 Series": {"variants": ["320d Luxury Line", "330i M Sport", "320d Sport"], "base_price": 4800000, "engine": 1995, "mileage": 16.1, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5},
        "5 Series": {"variants": ["520d Luxury Line", "530d M Sport"], "base_price": 6500000, "engine": 1995, "mileage": 17.4, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5},
        "X1": {"variants": ["sDrive20d", "sDrive20i"], "base_price": 4200000, "engine": 1995, "mileage": 16.3, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5}
    },
    "Mercedes-Benz": {
        "C-Class": {"variants": ["C 220d", "C 200", "C 300d"], "base_price": 5500000, "engine": 1993, "mileage": 16.9, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5},
        "E-Class": {"variants": ["E 220d", "E 200", "E 350d"], "base_price": 7200000, "engine": 1993, "mileage": 15.0, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5},
        "GLC": {"variants": ["GLC 220d", "GLC 300"], "base_price": 6200000, "engine": 1993, "mileage": 14.7, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5}
    },
    "Audi": {
        "A4": {"variants": ["40 TFSI Premium", "40 TFSI Technology"], "base_price": 4600000, "engine": 1984, "mileage": 17.4, "fuels": ["Petrol"], "transmissions": ["Automatic"], "seats": 5},
        "A6": {"variants": ["45 TFSI Premium Plus", "45 TFSI Technology"], "base_price": 6200000, "engine": 1984, "mileage": 14.1, "fuels": ["Petrol"], "transmissions": ["Automatic"], "seats": 5},
        "Q3": {"variants": ["35 TDI Quattro", "40 TFSI"], "base_price": 4300000, "engine": 1984, "mileage": 15.8, "fuels": ["Petrol", "Diesel"], "transmissions": ["Automatic"], "seats": 5}
    }
}

LOCATIONS = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Pune", "Ahmedabad", "Kolkata", "Jaipur", "Chandigarh", "Vadodara", "Surat", "Kochi", "Lucknow"]
OWNERS = ["1st Owner", "2nd Owner", "3rd Owner", "4+ Owners"]
CONDITIONS = ["Excellent", "Good", "Fair", "Poor"]

CURRENT_YEAR = 2026

def generate_records(num_records=2750):
    records = []
    
    brands = list(CAR_CATALOG.keys())
    
    for _ in range(num_records):
        brand = random.choice(brands)
        model = random.choice(list(CAR_CATALOG[brand].keys()))
        spec = CAR_CATALOG[brand][model]
        
        variant = random.choice(spec["variants"])
        year = random.randint(2013, 2024)
        age = CURRENT_YEAR - year
        
        fuel_type = random.choice(spec["fuels"])
        transmission = random.choice(spec["transmissions"])
        seats = spec["seats"]
        
        # Kilometers driven based on age
        annual_km = random.randint(6000, 15000)
        km_driven = max(3000, age * annual_km + random.randint(-4000, 5000))
        
        engine_cc = spec["engine"] + random.choice([-50, 0, 50]) if spec["engine"] < 2000 else spec["engine"]
        mileage = round(spec["mileage"] + random.uniform(-1.5, 1.5), 1)
        
        ownership = random.choice(OWNERS)
        location = random.choice(LOCATIONS)
        condition = random.choice(CONDITIONS)
        insurance_valid = random.choice([True, False])
        
        # Price Calculation Logic based on realistic depreciation curves
        base_val = spec["base_price"]
        
        # Age depreciation (approx 10-12% per year)
        depreciation = (0.88 ** age)
        
        # KM impact
        km_factor = 1.0 - (km_driven / 300000.0) * 0.35
        km_factor = max(0.45, km_factor)
        
        # Transmission bonus
        trans_factor = 1.08 if transmission == "Automatic" else 1.0
        
        # Ownership penalty
        owner_weights = {"1st Owner": 1.0, "2nd Owner": 0.88, "3rd Owner": 0.78, "4+ Owners": 0.68}
        owner_factor = owner_weights[ownership]
        
        # Condition factor
        cond_weights = {"Excellent": 1.05, "Good": 1.0, "Fair": 0.88, "Poor": 0.73}
        cond_factor = cond_weights[condition]
        
        # Insurance small bonus
        ins_factor = 1.02 if insurance_valid else 0.98
        
        # Random noise (+/- 5%)
        noise = random.uniform(0.95, 1.05)
        
        calculated_price = base_val * depreciation * km_factor * trans_factor * owner_factor * cond_factor * ins_factor * noise
        
        # Floor price logic
        floor_price = 120000 if base_val < 1000000 else 350000
        final_price = max(floor_price, int(round(calculated_price / 5000.0) * 5000))
        
        records.append({
            "brand": brand,
            "model": model,
            "variant": variant,
            "year": year,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "km_driven": km_driven,
            "engine_cc": engine_cc,
            "mileage": mileage,
            "ownership": ownership,
            "location": location,
            "seats": seats,
            "condition": condition,
            "insurance_valid": insurance_valid,
            "price": final_price
        })
        
    return records

if __name__ == "__main__":
    records = generate_records(2750)
    fieldnames = ["brand", "model", "variant", "year", "fuel_type", "transmission", "km_driven", "engine_cc", "mileage", "ownership", "location", "seats", "condition", "insurance_valid", "price"]
    
    out_path = "data/raw/cars.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Dataset successfully created at '{out_path}' with {len(records)} records.")
