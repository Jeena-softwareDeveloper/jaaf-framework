import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import settings
from main import db
from core.agents import get_dynamic_agent_response, run_hierarchical_strategy
from core.logger_setup import jaaf_logger as logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ceo_config = db.get_ceo_config()
    role = ceo_config.get("role", "Master Controller CEO")
    welcome_text = (
        f"👑 *Jeenora Personal CEO Activated*\n\n"
        f"I am your all-in-one A to Z Personal Assistant.\n"
        f"I have direct access to your local workstation and global web tools.\n\n"
        f"🚀 *My Capabilities:*\n"
        f"• 🌐 Deep Website & SEO Analysis\n"
        f"• 📂 Source Code (GitHub) Inspection\n"
        f"• 💻 Real-time System Health Monitoring\n"
        f"• 🐍 Python Logic Execution\n"
        f"• 🌤️ Live Weather & Market Trends\n"
        f"• 📈 Multi-Department Business Strategy\n\n"
        f"➡️ /strategy - Global Analysis\n"
        f"➡️ /status - Workstation Health\n"
        f"➡️ Just chat with me for anything else!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def check_health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from tools.external import ExternalTools
    await update.message.reply_text("💾 *Fetching Workstation Health Status...*", parse_mode="Markdown")
    stats = ExternalTools.get_system_health()
    logger.info(f"[/status] Health check requested by {update.message.chat_id}")
    await update.message.reply_text(stats, parse_mode="Markdown")

async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📋 /logs command — show last 20 lines from jaaf_master.log."""
    from tools.external import ExternalTools
    logger.info(f"[/logs] Log dump requested by {update.message.chat_id}")
    log_data = ExternalTools.check_logs(lines=20)
    await update.message.reply_text(
        f"📋 *JAAF System Log (last 20 entries):*\n```\n{log_data[:3800]}\n```",
        parse_mode="Markdown"
    )

async def run_strategy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ *Initializing Global Strategy Orchestration*... Deploying sub-agents. Please wait.", parse_mode="Markdown")
    try:
        ceo_config = db.get_ceo_config()
        snapshot = db.get_all_business_snapshot()
        
        report = await run_hierarchical_strategy(ceo_config, snapshot)
        
        final_msg = f"🌟 *Jeenora Global Strategy Report* 🌟\n\n{str(report)[:4000]}"
        await msg.edit_text(final_msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error running strategy: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = str(update.message.chat_id)

    if str(settings.TELEGRAM_CHAT_ID) != "YOUR_CHAT_ID_HERE" and str(settings.TELEGRAM_CHAT_ID) != chat_id:
        logger.warning(f"[Bot] Unauthorized access attempt from Chat ID: {chat_id}")
        await update.message.reply_text("❌ Unauthorized. You are not the registered Master Controller.")
        return

    logger.info(f"[Bot] Message received: '{user_text[:60]}...' from {chat_id}")

    # Define the Status Callback for real-time updates
    status_msg_obj = None
    async def status_callback(text):
        nonlocal status_msg_obj
        try:
            if status_msg_obj is None:
                status_msg_obj = await update.message.reply_text(text, parse_mode="Markdown")
            else:
                await status_msg_obj.edit_text(text, parse_mode="Markdown")
        except: pass

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        ceo_config = db.get_ceo_config()
        role = ceo_config.get("role", "Master Controller CEO")
        goal = ceo_config.get("goal", "Run Jeenora effectively")
        backstory = ceo_config.get("backstory", "You are the highest authority AI.")
        model = ceo_config.get("model", "gpt-oss:120b-cloud")
        temperature = ceo_config.get("temperature", 0.7)

        # Inject real-time business data snapshot into the prompt
        snapshot = db.get_all_business_snapshot()
        context_prompt = (
            f"You are speaking directly to your human supervisor (the company owner) via Telegram.\n"
            f"Current Real-Time Business Data Snapshot:\n{snapshot}\n\n"
            f"User Message:\n{user_text}\n\n"
            f"REMINDER: DO NOT STOP until the user's task is fully analyzed/complete."
        )
        
        reply = await get_dynamic_agent_response(
            role, 
            goal, 
            backstory, 
            context_prompt, 
            model, 
            temperature,
            target_url=ceo_config.get("target_url", ""),
            git_repo=ceo_config.get("git_repo", ""),
            status_callback=status_callback
        )
        
        # Cleanup status message before final reply
        if status_msg_obj:
            try: await status_msg_obj.delete()
            except: pass

        # Telegram has a 4096 character limit
        for i in range(0, len(reply), 4000):
            await update.message.reply_text(reply[i:i+4000])
        logger.info(f"[Bot] Reply sent to {chat_id} ({len(reply)} chars).")
    except Exception as e:
        logger.error(f"[Bot] handle_message ERROR: {e}")
        await update.message.reply_text(f"❌ Error generating response: {str(e)}")

def main():
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("TELEGRAM_BOT_TOKEN not set in .env!")
        return

    logger.info("🤖 JAAF Telegram Bot Starting — Listening for owner messages.")
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("strategy", run_strategy))
    app.add_handler(CommandHandler("status", check_health))
    app.add_handler(CommandHandler("logs", show_logs))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
