from pymongo import MongoClient
from config import settings

class JeenoraDB:
    def __init__(self):
        try:
            self.client = MongoClient(settings.MONGO_URI)
            self.db = self.client[settings.DB_NAME]
            print(f"Connected to MongoDB: {settings.DB_NAME}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_agri_summary(self):
        return self.db.agri_orders.count_documents({"status": "pending"})

    def get_dress_inventory_status(self):
        low_stock_items = list(self.db.cloths.find({"stock": {"$lt": 10}}))
        return len(low_stock_items)

    def get_crm_leads(self):
        return self.db.leads.count_documents({"replied": False})

    def get_all_business_snapshot(self):
        return {
            "agri_pending": self.get_agri_summary(),
            "low_stock_dresses": self.get_dress_inventory_status(),
            "new_crm_leads": self.get_crm_leads()
        }

    def get_order_status(self, order_id):
        # Example: Fetch order info by ID
        order = self.db.orders.find_one({"order_id": order_id})
        if order:
            return f"Order {order_id} is currently: {order.get('status', 'Processing')}"
        return "Order not found."

    def get_product_list(self, category):
        # Example: Fetch top items in a category
        products = list(self.db[category].find().limit(5))
        return [p.get('name') for p in products]
