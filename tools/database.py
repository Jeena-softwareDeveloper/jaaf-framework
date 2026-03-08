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

    def get_agents(self):
        """Fetches all agent configurations."""
        agents = list(self.db.agents.find())
        for a in agents:
            a["id"] = str(a.pop("_id"))
        return agents

    def get_agent(self, agent_id):
        """Fetches a single agent by ID."""
        from bson import ObjectId
        agent = self.db.agents.find_one({"_id": ObjectId(agent_id)})
        if agent:
            agent["id"] = str(agent.pop("_id"))
        return agent

    def save_agent(self, agent_data):
        """Saves or updates an agent configuration."""
        from bson import ObjectId
        agent_id = agent_data.pop("id", None)
        if agent_id:
            self.db.agents.update_one({"_id": ObjectId(agent_id)}, {"$set": agent_data}, upsert=True)
            return agent_id
        else:
            result = self.db.agents.insert_one(agent_data)
            return str(result.inserted_id)

    def delete_agent(self, agent_id):
        """Deletes an agent configuration."""
        from bson import ObjectId
        return self.db.agents.delete_one({"_id": ObjectId(agent_id)}).deleted_count > 0

    def get_ceo_config(self):
        """Legacy support for CEO - fetches the agent marked as CEO or returns defaults."""
        ceo = self.db.agents.find_one({"role": {"$regex": "CEO", "$options": "i"}})
        if ceo:
            ceo["id"] = str(ceo.pop("_id"))
            return ceo
        return {
            "name": "Jeenora CEO",
            "role": "Jeenora Group CEO",
            "goal": "Ensure overall profit and business growth.",
            "backstory": "You are the digital CEO of Jeenora.",
            "model": "gpt-oss:120b-cloud",
            "temperature": 0.7
        }
