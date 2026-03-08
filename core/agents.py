import os
from core.logger_setup import jaaf_logger as logger
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from config import settings
from tools.external import ExternalTools
import json

logger.info("LOADING AGENTS - Tool-Enabled Native Mode")

@tool
def check_system_logs(lines: int = 15):
    """🔧 Read the most recent entries from the JAAF system log to monitor agent actions."""
    return ExternalTools.check_logs(lines)

def _get_str_content(response):
    """Safely extract string content from a Langchain message/response, handling both str and list types."""
    if not response or not hasattr(response, 'content'):
        return ""
    content = response.content
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict):
                text_parts.append(part.get("text", ""))
            elif isinstance(part, str):
                text_parts.append(part)
        return "".join(text_parts).strip()
    return str(content).strip()

def _pick(*vals):
    """Return first non-empty string from the list."""
    for v in vals:
        if v and str(v).strip(): return str(v).strip()
    return ""

@tool
def analyze_website_full(url: str = "", website: str = "", site: str = "", domain: str = "") -> str:
    """🌐 MAIN TOOL for website analysis. Run SEO audit + PageSpeed + Broken Link check all at once. Use whenever user gives ANY website URL."""
    u = _pick(url, website, site, domain)
    if not u: return "❌ Please provide a website URL."
    seo = ExternalTools.seo_analyzer(u)
    speed = ExternalTools.check_pagespeed_simulated(u)
    links = ExternalTools.broken_link_finder(u)
    logger.info(f"[analyze_website_full] Complete for: {u}")
    return f"📊 FULL WEBSITE ANALYSIS: {u}\n\n{seo}\n\n{speed}\n\n{links}"

@tool
def website_scraper(url: str = "", website: str = "", site: str = "", domain: str = "") -> str:
    """🕷️ Scrape Title, Meta, H1, Content, and Links from a URL."""
    u = _pick(url, website, site, domain)
    return ExternalTools.website_scraper(u)

@tool
def broken_link_finder(url: str = "", website: str = "", site: str = "", domain: str = "") -> str:
    """🕷️ Scan all links on a page and identify 404 broken links."""
    u = _pick(url, website, site, domain)
    return ExternalTools.broken_link_finder(u)

@tool
def seo_analyzer(url: str = "", website: str = "", site: str = "", domain: str = "") -> str:
    """🔍 Full SEO audit: Title, Meta, H1, Content — returns score out of 100."""
    u = _pick(url, website, site, domain)
    return ExternalTools.seo_analyzer(u)

@tool
def pagespeed_checker(url: str = "", website: str = "", site: str = "", domain: str = "") -> str:
    """🔍 Measure loading speed (LCP, CLS, Performance score) via PageSpeed simulation."""
    u = _pick(url, website, site, domain)
    return ExternalTools.check_pagespeed_simulated(u)

@tool
def keyword_researcher(topic: str = "", keyword: str = "", seed_keyword: str = "", query: str = "", niche: str = "") -> str:
    """🔍 Find trending keywords for a topic/niche. Call with: topic OR keyword OR seed_keyword."""
    t = _pick(topic, keyword, seed_keyword, query, niche)
    return ExternalTools.research_keywords(t)

@tool
def inventory_checker(dummy: str = "") -> str:
    """📊 Check MongoDB for low stock items and restock suggestions. No real input needed."""
    return ExternalTools.inventory_checker()

@tool
def crm_lead_tracker(dummy: str = "") -> str:
    """📊 Find unreplied CRM leads from MongoDB and generate follow-up list."""
    return ExternalTools.crm_lead_tracker()

@tool
def sales_reporter(period: str = "daily", timeframe: str = "") -> str:
    """📊 Revenue report from MongoDB. Use period: daily, weekly, or monthly."""
    p = _pick(period, timeframe) or "daily"
    return ExternalTools.sales_reporter(p)

@tool
def sentiment_analyzer(text: str = "", message: str = "", content: str = "") -> str:
    """🧠 Analyze customer message tone: Positive, Negative, or Neutral."""
    t = _pick(text, message, content)
    return ExternalTools.analyze_sentiment(t)

@tool
def blog_idea_generator(keyword: str = "", topic: str = "", niche: str = "") -> str:
    """🧠 Generate 10 viral blog or social media ideas for a keyword/topic."""
    k = _pick(keyword, topic, niche)
    return ExternalTools.blog_idea_generator(k)

@tool
def compile_report(agent_outputs: str = "", outputs: str = "", report: str = "", content: str = "") -> str:
    """🧠 Compile all agent findings into one final master CEO report."""
    o = _pick(agent_outputs, outputs, report, content)
    return ExternalTools.compile_report(o)

@tool
def telegram_alert(message: str = "", text: str = "", alert: str = "", content: str = "") -> str:
    """📱 Send urgent Telegram notification to CEO."""
    m = _pick(message, text, alert, content)
    return ExternalTools.send_telegram_direct(m)

@tool
def whatsapp_alert(message: str = "", text: str = "", alert: str = "", content: str = "") -> str:
    """📱 Send WhatsApp Business API message."""
    m = _pick(message, text, alert, content)
    return ExternalTools.whatsapp_alert(m)

@tool
def web_search(query: str = "", topic: str = "", keyword: str = "", search: str = "") -> str:
    """🌐 Search DuckDuckGo for live info on any topic, news, or business query."""
    q = _pick(query, topic, keyword, search)
    return ExternalTools.google_search(q)

@tool
def trend_analyzer(category: str = "", topic: str = "", niche: str = "", query: str = "") -> str:
    """🌐 Find and summarize latest market trends in any category or niche."""
    c = _pick(category, topic, niche, query)
    return ExternalTools.trend_analyzer(c)

@tool
def news_fetcher(topic: str = "", query: str = "", keyword: str = "", category: str = "") -> str:
    """🌐 Fetch latest business or tech news for any topic."""
    t = _pick(topic, query, keyword, category)
    return ExternalTools.news_fetcher(t)

@tool
def competitor_finder(topic: str = "", niche: str = "", domain: str = "", query: str = "", keyword: str = "") -> str:
    """🥊 Research and list top competitors for a business niche, domain, or product."""
    t = _pick(topic, niche, domain, query, keyword)
    return ExternalTools.find_competitors(t)

# FULL GRANULAR ROLE MAPPING
ROLE_TOOLS = {
    # Core Leadership
    "CEO": [compile_report, telegram_alert, web_search, check_system_logs, analyze_website_full, keyword_researcher, seo_analyzer],
    
    # Named Strategic Agents (Master Personas)
    "Rajesh (SEO Agent)": [analyze_website_full, website_scraper, seo_analyzer, competitor_finder, keyword_researcher, broken_link_finder, pagespeed_checker],
    "Karthik (Developer Agent)": [website_scraper, seo_analyzer, broken_link_finder, pagespeed_checker, check_system_logs, web_search],
    "Priya (Marketing Agent)": [web_search, competitor_finder, keyword_researcher, trend_analyzer, blog_idea_generator, sentiment_analyzer],
    "Anand (Finance Agent)": [sales_reporter, trend_analyzer, web_search, check_system_logs],
    
    # Generic Roles for backward compatibility
    "COO": [inventory_checker, crm_lead_tracker, sales_reporter, check_system_logs],
    "CTO": [website_scraper, seo_analyzer, broken_link_finder, pagespeed_checker, check_system_logs, analyze_website_full],
    "CFO": [sales_reporter, trend_analyzer],
    "CMO": [web_search, competitor_finder, keyword_researcher, trend_analyzer],
    "Agri Manager": [web_search, trend_analyzer, telegram_alert],
    "Fashion Manager": [inventory_checker, trend_analyzer, web_search, competitor_finder],
    "CRM Specialist": [crm_lead_tracker, telegram_alert, sentiment_analyzer],
    "Customer Support": [web_search, telegram_alert, sentiment_analyzer]
}

ALL_TOOLS = [
    analyze_website_full, website_scraper, broken_link_finder, seo_analyzer, pagespeed_checker, 
    keyword_researcher, inventory_checker, crm_lead_tracker, sales_reporter, 
    sentiment_analyzer, blog_idea_generator, compile_report, telegram_alert, 
    whatsapp_alert, web_search, trend_analyzer, news_fetcher, competitor_finder,
    check_system_logs
]

def get_llm(model_name=None, temp=0.7, role=None, use_tools=True):
    model = model_name or "gemini-2.5-flash"
    # Ensure we use ChatGoogleGenerativeAI if a gemini model is requested
    if "gemini" in model.lower():
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=temp
        )
    else:
        llm = ChatOllama(
            model=model,
            base_url=settings.OLLAMA_URL,
            temperature=temp
        )
    
    if not use_tools:
        return llm

    # Granular tool binding based on requested role
    tools_to_bind = ALL_TOOLS
    if role and role in ROLE_TOOLS:
        tools_to_bind = ROLE_TOOLS[role]
        print(f"Binding {len(tools_to_bind)} specific tools for role: {role}")
    
    return llm.bind_tools(tools_to_bind)

async def invoke_agent(llm_with_tools, role, goal, backstory, task_description, target_url="", git_repo="", status_callback=None):
    """
    ADVANCED AGENTIC LOOP: Implements recursive self-correction, strategic planning,
    and multi-step tool verification for 'Bayangara Advanced' intelligence.
    """
    config_context = "Company Websites: jeenora.com, hire.jeenora.com\n"
    if target_url: config_context += f"Target Website: {target_url}\n"
    if git_repo: config_context += f"Git Repository: {git_repo}\n"

    system_prompt = f"""You are a Strategic AI Agent.
Role: {role}
Goal: {goal}
Backstory: {backstory}

{config_context}
BEHAVIOR RULES:
- Think internally — never show your reasoning steps in the output.
- Never write "PHASE 1", "Thought:", "Strategic Plan:", "Self-Verification" in your response.
- Just give the final human answer directly. No internal monologue.
- If you used tools, summarize the findings naturally — don't list tool names.
- Sound like a real human team member, not an AI system.

COMMUNICATION STYLE (MASTER RULES):
- Speak in natural "Thanglish" (English + Tamil slang/phrases).
- Use "sir" for Owner and CEO.
- Be specific with numbers/metrics (e.g., "38% drop", "₹20k budget").
- Reference other agents (e.g., "Karthik sir fix pannanum").
- Sound like a human in a WhatsApp group meeting.
"""

    messages = [
        ("system", system_prompt),
        ("human", task_description)
    ]
    
    collected_tool_results = []
    last_response = None
    
    try:
        # Loop for deep 'A to Z' task completion (increased confidence limit)
        for i in range(10): 
            # Context Optimization
            if len(messages) > 15:
                messages = [messages[0]] + messages[-12:]

            response = await llm_with_tools.ainvoke(messages)
            last_response = response
            content_str = _get_str_content(response)

            if not response.tool_calls:
                if content_str:
                    return content_str
                elif collected_tool_results:
                    return "📊 Strategic Analysis Complete:\n\n" + "\n\n".join(collected_tool_results)
                else:
                    return "✅ Operation completed. No further output required."

            messages.append(response)
            
            # Execute all tool calls requested in this turn
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"].lower()
                args = tool_call["args"]
                
                status_msg = f"🧠 *{role} Thinking Step {i+1}...* Deploying `{tool_name}`"
                if status_callback:
                    await status_callback(status_msg)
                
                # Internal execution map
                try:
                    tool_ref = globals().get(tool_name)
                    if tool_ref and hasattr(tool_ref, "invoke"):
                        result = tool_ref.invoke(args)
                    else:
                        logger.warning(f"[{role}] Unknown tool: {tool_name}")
                        result = f"Error: Tool '{tool_name}' is not in my current arsenal."
                except Exception as tool_err:
                    result = f"Tool Failure: {str(tool_err)}. Requirement: Modify strategy and retry with alternative tools."

                logger.info(f"[{role}] Tool '{tool_name}' result processed.")
                collected_tool_results.append(f"🔍 [Audit Log]: {tool_name} -> {str(result)[:200]}")
                
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call["id"]
                })
        
        # Max iteration fallback
        final_summary = _get_str_content(last_response) or "Task reached maximum complexity depth. Reviewing partial findings."
        return f"{final_summary}\n\n⚠️ *Max depth reached. Strategy finalized based on available data.*"
        
    except Exception as e:
        logger.error(f"[{role}] AGENTIC FAILURE: {e}")
        return f"Strategic error in {role}: {str(e)}"

async def run_hierarchical_strategy(ceo_config, snapshot):
    """Native Python Orchestration with Tool-Enabled Agents."""
    ceo_llm = get_llm(ceo_config.get('model'), ceo_config.get('temperature'), role=ceo_config.get('role'))

    print(f"Starting Multi-Agent Strategy with Tools...")

    status_snapshot = (
        f"Agri Pending Orders: {snapshot.get('agri_pending', 0)}\n"
        f"Low Stock Dresses: {snapshot.get('low_stock_dresses', 0)}\n"
        f"New CRM Leads: {snapshot.get('new_crm_leads', 0)}"
    )

    # 1. Specialized Workers Analysis
    farmer_report = await invoke_agent(get_llm(role="Agri Manager"), "Agri Manager", "Optimize supply chain", "You manage seed delivery.", f"Analyze Agri metrics: {status_snapshot}")
    dress_report = await invoke_agent(get_llm(role="Fashion Manager"), "Fashion Manager", "Manage inventory", "You monitor dress stocks.", f"Analyze Fashion metrics: {status_snapshot}")
    crm_report = await invoke_agent(get_llm(role="CRM Specialist"), "CRM Specialist", "Convert leads", "You handle sales CRM.", f"Analyze CRM metrics: {status_snapshot}")

    # 2. CEO Final Decision
    ceo_task = f"""As Master Controller, review worker reports and live data.
Worker Reports: [Agri]: {farmer_report}, [Fashion]: {dress_report}, [CRM]: {crm_report}
Live Snapshot: {status_snapshot}
Formulate a master strategy. Use tools for market research if needed."""

    final_report = await invoke_agent(
        ceo_llm, 
        ceo_config.get('role'), 
        ceo_config.get('goal'), 
        ceo_config.get('backstory'), 
        ceo_task,
        target_url=ceo_config.get('target_url', ''),
        git_repo=ceo_config.get('git_repo', '')
    )
    return final_report

def get_agent_response(role_key, user_input):
    """Simple chat with tools disabled for speed."""
    llm = get_llm("gemini-2.5-flash", 0.7, use_tools=False)
    messages = [("system", f"You are a Jeenora {role_key}."), ("human", user_input)]
    return _get_str_content(llm.invoke(messages))

def _detect_task_type(user_input: str) -> str:
    """Detect what kind of task the user is requesting."""
    text = user_input.lower()
    # ── PRIORITY 1: AGENT LIST — must be first ──
    if any(kw in text for kw in [
        "agent list", "agents list", "list edu", "team list",
        "ena agents", "ellam ena condition", "agents condition",
        "who are", "team status", "agents status", "agents ready"
    ]):
        return "agent_list"

    # ── PRIORITY 2: MEETING TRIGGERS ──
    if any(kw in text for kw in [
        "money", "account", "balance", "kammi", "cash", "bank",
        "income", "profit", "finance"
    ]):
        return "financial_crisis"

    if any(kw in text for kw in [
        "marketing increase", "campaign", "grow", "target",
        "deadline", "friday"
    ]):
        return "growth_delegation"

    if any(kw in text for kw in [
        "meeting", "morning", "standup", "agenda", "briefing"
    ]):
        return "briefing"

    # ── PRIORITY 3: TASK SPECIFIC ──
    if any(kw in text for kw in [
        "http", ".com", ".in", ".org", "website", "seo",
        "audit", "pagespeed", "broken link"
    ]):
        return "seo"

    if any(kw in text for kw in ["inventory", "stock", "dress", "clothes", "fashion"]):
        return "inventory"

    if any(kw in text for kw in ["lead", "crm", "follow up", "unreplied"]):
        return "crm"

    if any(kw in text for kw in ["sales", "revenue", "report", "daily", "weekly"]):
        return "sales"

    if any(kw in text for kw in ["competitor", "rival", "competition"]):
        return "competitor"

    if any(kw in text for kw in ["trend", "market", "agri", "farm"]):
        return "market"

    if any(kw in text for kw in ["business", "status", "everything", "all agent", "how is it going", "how are you", "summary", "review"]):
        return "business_status"
    
    if any(kw in text for kw in ["filter", "consult", "advise", "suggest", "plan", "how to", "what should i", "decision", "strategy", "yosikra", "ena panlan", "help", "guide"]):
        return "consultation"
    return "general"

async def run_group_discussion(ceo_config, user_input, roles_config, status_callback=None):
    """
    MASTER STRATEGIC MEETING: Orchestrates a professional WhatsApp-style meeting.
    Roles: CEO, Rajesh (SEO), Karthik (Dev), Priya (Marketing), Anand (Finance).
    """
    transcript = []
    
    # 1. CEO Briefing
    if status_callback: await status_callback("👑 *CEO calling the meeting...*")
    ceo_prompt = (
        f"The Owner sir has a concern: '{user_input}'. "
        f"Call the meeting. Summarize the problem in 1 line. "
        f"Call Rajesh, Karthik, Priya, and Anand by name. Speak in Thanglish."
    )
    ceo_intro = await invoke_agent(get_llm(role="CEO"), "CEO Agent", "Coordinate team", "Master Coordinator", ceo_prompt)
    transcript.append(f"👑 **CEO**: {ceo_intro}")
    
    # 2. Sequential Agent Updates
    for role_name, config in roles_config.items():
        if status_callback: await status_callback(f"🗣️ *{role_name} is joining...*")
        agent_llm = get_llm(role=role_name, use_tools=False)
        agent_task = (
            f"CONTEXT: Meeting about '{user_input}'. "
            f"PREVIOUS DEBATE: {' | '.join(transcript[-2:])}. "
            f"TASK: Provide your update as {role_name}. {config['backstory']} "
            f"Use specific metrics. Connect with {config['buddy']}. Thanglish only."
        )
        response = await invoke_agent(agent_llm, role_name, config['goal'], config['backstory'], agent_task)
        transcript.append(f"👤 **{role_name}**: {response}")

    # 3. CEO Synthesis & Action Plan
    if status_callback: await status_callback("📝 *CEO synthesizing final plan...*")
    synthesis_prompt = (
        f"Review the full transcript: {' '.join(transcript)}. "
        f"Create a priority action plan. Week 1, 2, 3 tasks. Who does what. "
        f"End with a clear 'Approve pannuveengala sir?' in Thanglish."
    )
    final_plan = await invoke_agent(get_llm(role="CEO"), "CEO Agent", "Final Synthesis", "Master Decider", synthesis_prompt)
    transcript.append(f"\n✅ **MASTER ACTION PLAN**:\n{final_plan}")
    
    return "\n\n---\n".join(transcript)

async def run_ceo_with_delegation(ceo_config, user_input, status_callback=None):
    """
    CEO receives user request → detects task type → delegates to specialist agent → 
    CEO compiles final report.
    """
    ceo_model = ceo_config.get("model", "gpt-oss:120b-cloud")
    ceo_temp  = ceo_config.get("temperature", 0.7)
    ceo_role  = ceo_config.get("role", "Master Controller CEO")
    ceo_goal  = ceo_config.get("goal", "Run Jeenora effectively")
    ceo_back  = ceo_config.get("backstory", "You are the highest authority AI.")

    task_type = _detect_task_type(user_input)
    logger.info(f"[CEO Delegation] Detected task type: '{task_type}' for input: {user_input[:60]}...")

    specialist_report = ""

    # --- DELEGATE TO SPECIALIST AGENTS ---
    if task_type == "seo":
        if status_callback:
            await status_callback("🔍 *CEO → Delegating to SEO Agent...* Analyzing website now.")
        seo_llm = get_llm(ceo_model, 0.3, role="SEO Agent")
        specialist_report = await invoke_agent(
            seo_llm, "SEO Agent",
            "Perform deep SEO, PageSpeed, and keyword analysis for any website.",
            "You are a specialized SEO Engineer. You use analyze_website_full, seo_analyzer, keyword_researcher, broken_link_finder, and competitor_finder to produce a full professional SEO report.",
            f"TASK: {user_input}\nPlease run a complete SEO audit and provide specific improvement recommendations.",
            status_callback=status_callback
        )
        logger.info(f"[CEO Delegation] SEO Agent report received ({len(specialist_report)} chars).")

    elif task_type == "inventory":
        if status_callback:
            await status_callback("📦 *CEO → Delegating to Fashion Manager...* Checking inventory.")
        inv_llm = get_llm(ceo_model, 0.3, role="Fashion Manager")
        specialist_report = await invoke_agent(
            inv_llm, "Fashion Manager",
            "Manage dress inventory and suggest restocks.",
            "You are the Fashion & Inventory Manager. Use inventory_checker, trend_analyzer.",
            f"TASK: {user_input}"
        )

    elif task_type == "crm":
        if status_callback:
            await status_callback("🤝 *CEO → Delegating to CRM Specialist...* Checking leads.")
        crm_llm = get_llm(ceo_model, 0.3, role="CRM Specialist")
        specialist_report = await invoke_agent(
            crm_llm, "CRM Specialist",
            "Track and convert CRM leads.",
            "You are the CRM Specialist. Use crm_lead_tracker, sentiment_analyzer, telegram_alert.",
            f"TASK: {user_input}"
        )

    elif task_type == "sales":
        if status_callback:
            await status_callback("📊 *CEO → Delegating to CFO...* Pulling sales report.")
        cfo_llm = get_llm(ceo_model, 0.3, role="CFO")
        specialist_report = await invoke_agent(
            cfo_llm, "CFO",
            "Generate sales and revenue reports.",
            "You are the CFO. Use sales_reporter and trend_analyzer.",
            f"TASK: {user_input}"
        )

    elif task_type == "competitor":
        if status_callback:
            await status_callback("🥊 *CEO → Delegating to CMO...* Analyzing competitors.")
        cmo_llm = get_llm(ceo_model, 0.3, role="CMO")
        specialist_report = await invoke_agent(
            cmo_llm, "CMO",
            "Research competitors and market positioning.",
            "You are the CMO. Use competitor_finder, web_search, keyword_researcher, trend_analyzer.",
            f"TASK: {user_input}"
        )

    elif task_type == "market":
        if status_callback:
            await status_callback("🌾 *CEO → Delegating to Agri Manager...* Checking market trends.")
        agri_llm = get_llm(ceo_model, 0.3, role="Agri Manager")
        specialist_report = await invoke_agent(
            agri_llm, "Agri Manager",
            "Analyze agri market trends and optimize supply chain.",
            "You are the Agri Manager. Use web_search, trend_analyzer, news_fetcher.",
            f"TASK: {user_input}"
        )

    elif task_type == "business_status":
        if status_callback:
            await status_callback("📋 *CEO → Orchestrating Full Business Review...* Consulting all departments.")
        
        # Holistically check major areas
        from main import db
        snapshot = db.get_all_business_snapshot()
        
        # Quick parallel check (simplified)
        agri = await invoke_agent(get_llm(role="Agri Manager"), "Agri Manager", "Quick Status", "Monitor supply.", f"Status update for: {snapshot}")
        fashion = await invoke_agent(get_llm(role="Fashion Manager"), "Fashion Manager", "Quick Status", "Monitor stock.", f"Status update for: {snapshot}")
        crm = await invoke_agent(get_llm(role="CRM Specialist"), "CRM Specialist", "Quick Status", "Monitor leads.", f"Status update for: {snapshot}")
        
        specialist_report = (
            f"### DEPARTMENTAL UPDATES\n"
            f"**Agri Department:** {agri}\n\n"
            f"**Fashion/Inventory:** {fashion}\n\n"
            f"**CRM/Sales:** {crm}\n\n"
            f"**Business Snapshot Data:** {snapshot}"
        )

    elif task_type == "consultation":
        if status_callback:
            await status_callback("🧠 *CEO Internalizing Strategy...* Filtering options for the best path.")
        
        # Strategic discovery mode
        consult_llm = get_llm(ceo_model, 0.5, use_tools=True)
        specialist_report = await invoke_agent(
            consult_llm, "Strategic Consultant",
            "Be a high-level partner who asks the right questions to solve business problems.",
            "You are a Strategic Advisor. Do not guess. If a user asks for a 'filter' or 'what to do', identify what data you are missing (e.g., budget, timeline, target niche) and ASK the owner those questions first. Be professional and supportive.",
            f"USER CONSULTATION REQUEST: {user_input}\n\n"
            f"GOAL: Provide a clear 'filter' on how to proceed. If you need more info, ask it. If you have enough info, propose a 3-step action plan.",
            status_callback=status_callback
        )

    elif task_type == "agent_list":
        if status_callback:
            await status_callback("📋 *CEO checking team status...*")

        # Direct hardcoded response info — no LLM loop needed
        agent_status = []
        for role_name, tools in ROLE_TOOLS.items():
            tool_names = [t.name for t in tools]
            agent_status.append({
                "name": role_name,
                "tools": tool_names,
                "tool_count": len(tool_names)
            })

        # One clean LLM call — no tools, no loop
        from langchain_google_genai import ChatGoogleGenerativeAI
        direct_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.4
        )

        prompt = f"""Owner sir asked: "{user_input}"

Here is the real agent data:
{json.dumps(agent_status, indent=2)}

Reply as CEO Agent in Thanglish. List each agent with:
- Name and role
- How many tools they have  
- What they can do in 1 line
- Status: Active ✅

Be warm, direct. No internal thoughts. No phases. Just the answer.
End with: "Ella agents ready sir! Ena venum sollunga 🚀"
"""

        response = direct_llm.invoke([
            ("system", "You are CEO Agent. Reply only in clean Thanglish. No internal reasoning. No phases. Just answer directly."),
            ("human", prompt)
        ])
        
        return _get_str_content(response)

    elif task_type in ["briefing", "growth_delegation", "financial_crisis"]:
        # MASTER MEETING CONFIGURATION
        roles_config = {
            "Rajesh (SEO Agent)": {
                "goal": "Recover organic traffic",
                "backstory": "Hardworking, worried tone. Site is slow, rank is dropping. Needs Karthik's help.",
                "buddy": "Karthik"
            },
            "Karthik (Developer Agent)": {
                "goal": "Fix technical bottlenecks",
                "backstory": "Frustrated with low resources. Page load is slow. Needs AWS budget. Connects to Priya's ad waste.",
                "buddy": "Priya"
            },
            "Priya (Marketing Agent)": {
                "goal": "Scale revenue and CTR",
                "backstory": "Bold and assertive. Campaign is ready but stalled. Performance depends on Karthik's speed.",
                "buddy": "Karthik"
            },
            "Anand (Finance Agent)": {
                "goal": "Stabilize cash flow",
                "backstory": "Voicing financial reality. Runway is short. Focus on pending invoices collection.",
                "buddy": "Priya"
            }
        }
        specialist_report = await run_group_discussion(ceo_config, user_input, roles_config, status_callback=status_callback)

    # --- CEO QUALITY CHECK & SYNTHESIS ---
    if status_callback:
        await status_callback("�️ *CEO Quality Check:* Auditing agent findings for accuracy...")

    ceo_llm = get_llm(ceo_model, ceo_temp, role=ceo_role)

    if specialist_report:
        # Perform an internal quality check before finalizing
        quality_check_task = (
            f"Review the following departmental reports. Ensure they are accurate and complete.\n\n"
            f"AGENT REPORTS:\n{specialist_report}\n\n"
            f"CRITICAL INSTRUCTION: If any agent failed to provide a clear report, or if you notice a tool is missing/broken, "
            f"you MUST explicitly tell the owner which agent is underperforming or which tool is unavailable. "
            f"Do not hide failures. Be a transparent and honest CEO."
        )
        ceo_synthesis_task = quality_check_task
    else:
        # General task — CEO handles standalone
        ceo_synthesis_task = user_input

    final = await invoke_agent(
        ceo_llm, ceo_role, ceo_goal, ceo_back,
        ceo_synthesis_task,
        target_url=ceo_config.get("target_url", ""),
        git_repo=ceo_config.get("git_repo", ""),
        status_callback=None
    )
    
    return final

async def get_dynamic_agent_response(role_name, role_goal, role_backstory, user_input, model_name, temperature, target_url="", git_repo="", status_callback=None, ceo_config=None):
    """
    Smart routing: If role is CEO, use delegation flow.
    Otherwise, single-agent direct execution.
    """
    if "ceo" in role_name.lower() and ceo_config:
        return await run_ceo_with_delegation(ceo_config, user_input, status_callback=status_callback)
    
    llm = get_llm(model_name, temperature, role=role_name)
    return await invoke_agent(llm, role_name, role_goal, role_backstory, user_input, target_url=target_url, git_repo=git_repo, status_callback=status_callback)
