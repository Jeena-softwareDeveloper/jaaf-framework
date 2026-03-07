import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import settings
from tools.database import JeenoraDB
from tools.external import ExternalTools
from core.agents import ceo_agent, farmer_agent, dress_agent, crm_agent, seo_agent, support_agent
from crewai import Task, Crew, Process

# FastAPI App
app = FastAPI(title="JAAF - Jeenora AI Agent Framework", version="1.0.0")

# CORS - Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Tools
db = JeenoraDB()
tools = ExternalTools()

# ========================
# 📊 API ENDPOINTS
# ========================

@app.get("/")
def health_check():
    return {"status": "JAAF is running", "version": "1.0.0"}

@app.get("/api/business/snapshot")
def get_business_snapshot():
    """Returns live MongoDB business stats for Dashboard."""
    try:
        snapshot = db.get_all_business_snapshot()
        return {"success": True, "data": snapshot}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/agents/status")
def get_agents_status():
    """Returns the status of all AI Agents."""
    return {
        "agents": [
            {"name": "CEO Agent", "role": "Business Strategist", "status": "active"},
            {"name": "Farmer Agent", "role": "Agri Manager", "status": "active"},
            {"name": "Dress Agent", "role": "Fashion Scout", "status": "active"},
            {"name": "CRM Agent", "role": "Lead Manager", "status": "active"},
            {"name": "SEO Agent", "role": "Market Intelligence", "status": "active"},
            {"name": "Support Agent", "role": "Customer Support", "status": "active"},
        ]
    }

class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
async def customer_chat(payload: ChatMessage):
    """Customer Support Chat - AI Reply."""
    support_task = Task(
        description=f"Reply to this customer query: {payload.message}",
        agent=support_agent,
        expected_output="A polite and helpful customer response."
    )
    crew = Crew(agents=[support_agent], tasks=[support_task])
    response = crew.kickoff()
    return {"success": True, "reply": str(response)}

@app.post("/api/ceo/run")
async def run_ceo_cycle():
    """Manually trigger the CEO Agent Business Cycle."""
    snapshot = db.get_all_business_snapshot()
    ceo_task = Task(
        description=f"Analyze: Agri({snapshot['agri_pending']}), Cloths({snapshot['low_stock_dresses']}), Leads({snapshot['new_crm_leads']}). Give strategy.",
        agent=ceo_agent,
        expected_output="CEO's strategic report."
    )
    crew = Crew(agents=[ceo_agent], tasks=[ceo_task])
    result = crew.kickoff()
    return {"success": True, "report": str(result)}
