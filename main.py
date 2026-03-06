import os
import asyncio
from config import settings
from tools.database import JeenoraDB
from tools.external import ExternalTools
from core.agents import ceo_agent, farmer_agent, dress_agent, crm_agent, seo_agent, support_agent
from crewai import Task, Crew, Process
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Initialize Tools
db = JeenoraDB()
tools = ExternalTools()

# --- JAAF CORE: BUSINESS CYCLE (Alerts & Reports) ---
async def run_jeenora_cycle():
    print("\n--- Starting Jeenora Business Cycle ---")
    snapshot = db.get_all_business_snapshot()
    
    competitor_task = Task(
        description=f"Identify competitors and provide a ranking roadmap for jeenora.com.",
        agent=seo_agent,
        expected_output="Competitor Benchmarking Report."
    )

    ceo_task = Task(
        description=f"Analyze current state: Agri({snapshot['agri_pending']}), Cloths({snapshot['low_stock_dresses']}), Leads({snapshot['new_crm_leads']}). Give strategy.",
        agent=ceo_agent,
        expected_output="CEO's daily strategic report."
    )

    jeenora_crew = Crew(
        agents=[ceo_agent, farmer_agent, dress_agent, crm_agent, seo_agent],
        tasks=[competitor_task, ceo_task],
        process=Process.hierarchical,
        manager_llm=ceo_agent.llm
    )

    result = jeenora_crew.kickoff()
    await tools.send_telegram_alert(f"📊 Jeenora CEO Report:\n\n{result}")
    return result

# --- JAAF INTERACTIVE: CUSTOMER CHAT HANDLER ---
async def handle_customer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(f"Customer Message: {user_msg}")

    # Use Support Agent to think and reply
    support_task = Task(
        description=f"Reply to this customer query based on Jeenora business values: {user_msg}. If they ask for order status, check if order_id is provided.",
        agent=support_agent,
        expected_output="A polite and helpful customer response."
    )
    
    # Fast Execution for Chat
    crew = Crew(agents=[support_agent], tasks=[support_task])
    response = crew.kickoff()
    
    await update.message.reply_text(response)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Jeenora AI Support. How can I help you today?")

# --- MAIN ENGINE LOOP ---
async def main():
    # 1. Setup Telegram Application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # 2. Add Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_customer_message))
    
    # 3. Start Telegram Bot Polling (Background)
    print("🤖 Jeenora Interactive Bot is Running...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # 4. Start 24/7 Business Loop (Concurrent)
    while True:
        try:
            await run_jeenora_cycle()
        except Exception as e:
            print(f"Error in business cycle: {e}")
        
        print(f"Sleeping for {settings.CHECK_INTERVAL} seconds...")
        await asyncio.sleep(settings.CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
