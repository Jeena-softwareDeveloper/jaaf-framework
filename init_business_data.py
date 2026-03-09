import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "jeenora_db"

def init_db():
    print(f"🚀 Initializing Jeenora Group Startup Baseline...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # 1. Load Business Config
    config_path = "config/business_config.json"
    with open(config_path, "r") as f:
        config_data = json.load(f)
    
    # 2. Update Business Snapshot (Tier 1 & Tier 6 use this)
    db.business_config.update_one(
        {"type": "baseline"},
        {"$set": config_data},
        upsert=True
    )
    print("✅ Business configuration uploaded.")

    # 3. Initialize Collections with Day 0 empty states
    # Finance
    db.finance_data.insert_one({
        "date": "2026-03-09",
        "revenue": 0,
        "expense": 0,
        "type": "initialization",
        "note": "Business start baseline"
    })
    
    # Inventory (Placeholders for Clothing and Agri)
    db.cloths.insert_many([
        {"name": "Cotton Shirt", "stock": 100, "price": 500, "category": "Clothes"},
        {"name": "Organic Rice (1kg)", "stock": 50, "price": 80, "category": "Agri"}
    ])
    
    # Leads
    db.leads.insert_one({
        "name": "Test Lead",
        "source": "Initial Setup",
        "status": "New",
        "replied": False
    })

    print("✅ All collections initialized with starting baseline.")
    client.close()

if __name__ == "__main__":
    init_db()
