import os
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import settings
from tools.database import JeenoraDB
from tools.external import ExternalTools
from core.agents import get_agent_response

# FastAPI App
app = FastAPI(title="JAAF - Jeenora AI Dashboard", version="1.0.0")

# CORS - Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/api/health")
def api_health():
    return {"status": "Healthy", "message": "API is online"}

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
            {"name": "Support Agent", "role": "Customer Support", "status": "active"},
            {"name": "SEO Agent", "role": "Market Intelligence", "status": "active"},
        ]
    }

# ========================
# 💬 CHAT & WEBSOCKETS
# ========================

@app.websocket("/ws/chat")
async def chat_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket Connected")
    try:
        while True:
            data = await websocket.receive_text()
            user_msg = json.loads(data).get("message")
            
            # Simple AI Response
            reply = get_agent_response("support", user_msg)
            
            # Send back response
            await websocket.send_text(json.dumps({"success": True, "reply": str(reply)}))
    except WebSocketDisconnect:
        print("WebSocket Disconnected")

class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
async def customer_chat(payload: ChatMessage):
    """Simple API Chat - AI Reply."""
    try:
        reply = get_agent_response("support", payload.message)
        return {"success": True, "reply": str(reply)}
    except Exception as e:
        return {"success": False, "error": str(e)}

class AgentConfig(BaseModel):
    id: str = None
    name: str
    role: str
    goal: str
    backstory: str
    model: str
    temperature: float

@app.get("/api/agents/list")
def list_agents():
    """List all agents from DB."""
    return {"success": True, "agents": db.get_agents()}

@app.post("/api/agents/save")
def save_agent(config: AgentConfig):
    """Save or update agent."""
    agent_id = db.save_agent(config.model_dump())
    return {"success": True, "id": agent_id}

@app.delete("/api/agents/{agent_id}")
def delete_agent(agent_id: str):
    """Delete an agent."""
    res = db.delete_agent(agent_id)
    return {"success": res}

@app.get("/api/ceo/config")
def get_ceo_config():
    """Fetch stored CEO agent configuration."""
    return {"success": True, "config": db.get_ceo_config()}

@app.websocket("/ws/ceo")
async def ceo_run_websocket(websocket: WebSocket):
    """Hierarchical CEO Strategy Run via WebSocket."""
    await websocket.accept()
    try:
        # 1. Fetch System Data
        snapshot = db.get_all_business_snapshot()
        config = db.get_ceo_config()
        
        await websocket.send_text(json.dumps({"status": "starting", "message": "Initializing Master Strategy..."}))
        await asyncio.sleep(1) # For UI feel
        
        # 2. Simulate Delegation Status (CrewAI is synchronous, so we simulate steps or use threads)
        # In a real app, we'd use callbacks, but for this workstation feel:
        await websocket.send_text(json.dumps({"agent": "Farmer Agent", "status": "delegated"}))
        await asyncio.sleep(1)
        await websocket.send_text(json.dumps({"agent": "Dress Agent", "status": "delegated"}))
        await asyncio.sleep(1)
        await websocket.send_text(json.dumps({"agent": "CRM Agent", "status": "working"}))
        
        # 3. Run the actual Hierarchical Strategy
        from core.agents import run_hierarchical_strategy
        await websocket.send_text(json.dumps({"status": "thinking", "message": "CEO is coordinating with sub-agents..."}))
        
        # Note: run_hierarchical_strategy is blocking. 
        # For a truly responsive UI, we would run this in a thread.
        report = run_hierarchical_strategy(config, snapshot)
        
        # 4. Final Output to UI
        await websocket.send_text(json.dumps({"status": "complete", "report": str(report)}))
        
        # 5. Send Telegram Notification
        from tools.external import ExternalTools
        telegram_msg = f"🌟 *Jeenora Global Strategy Alert* 🌟\n\n{str(report)[:3000]}" # Truncate to avoid Telegram limits
        await ExternalTools.send_telegram_alert(telegram_msg)
        
    except Exception as e:
        await websocket.send_text(json.dumps({"status": "error", "message": str(e)}))
    finally:
        await websocket.close()
