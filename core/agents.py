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
    "COO": [inventory_checker, crm_lead_tracker, sales_reporter, check_system_logs],
    "CTO": [website_scraper, seo_analyzer, broken_link_finder, pagespeed_checker, check_system_logs, analyze_website_full],
    "CFO": [sales_reporter, trend_analyzer],
    "CMO": [web_search, competitor_finder, keyword_researcher, trend_analyzer],
    
    # Tech & Development
    "Software Architect": [website_scraper, broken_link_finder, pagespeed_checker],
    "Full Stack Developer": [website_scraper, seo_analyzer, broken_link_finder],
    "Frontend Developer": [website_scraper, pagespeed_checker, seo_analyzer],
    "Backend Developer": [broken_link_finder, pagespeed_checker],
    "Mobile Developer": [web_search, trend_analyzer],
    "DevOps Engineer": [pagespeed_checker, broken_link_finder],
    "AI/ML Specialist": [web_search, trend_analyzer, sentiment_analyzer],
    "Data Scientist": [sales_reporter, trend_analyzer],
    "QA/Test Engineer": [broken_link_finder, pagespeed_checker, seo_analyzer],
    
    # Management & Product
    "Product Manager": [web_search, trend_analyzer, competitor_finder],
    "Project Manager": [compile_report, telegram_alert],
    "HR Manager": [web_search, telegram_alert],
    "Finance Manager": [sales_reporter, trend_analyzer],
    "Operations Manager": [inventory_checker, crm_lead_tracker],
    
    # Jeenora Specialized
    "Agri Manager": [web_search, trend_analyzer, telegram_alert],
    "Fashion Manager": [inventory_checker, trend_analyzer, web_search, competitor_finder],
    "CRM Specialist": [crm_lead_tracker, telegram_alert, sentiment_analyzer],
    "SEO Agent": [analyze_website_full, website_scraper, seo_analyzer, competitor_finder, keyword_researcher, broken_link_finder, pagespeed_checker],
    "Customer Support": [web_search, telegram_alert, sentiment_analyzer],
    
    # Marketing & Sales
    "Content Strategist": [web_search, keyword_researcher, blog_idea_generator, competitor_finder],
    "Social Media Manager": [web_search, trend_analyzer, sentiment_analyzer],
    "Sales Representative": [crm_lead_tracker, telegram_alert, web_search],
    "Growth Hacker": [web_search, competitor_finder, keyword_researcher, trend_analyzer],
    
    # Finance & Admin
    "Accountant": [sales_reporter],
    "Financial Analyst": [sales_reporter, trend_analyzer, web_search]
}

ALL_TOOLS = [
    analyze_website_full, website_scraper, broken_link_finder, seo_analyzer, pagespeed_checker, 
    keyword_researcher, inventory_checker, crm_lead_tracker, sales_reporter, 
    sentiment_analyzer, blog_idea_generator, compile_report, telegram_alert, 
    whatsapp_alert, web_search, trend_analyzer, news_fetcher, competitor_finder,
    check_system_logs
]

def get_llm(model_name=None, temp=0.7, role=None, use_tools=True):
    model = model_name or "gpt-oss:120b-cloud"
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
    """Native Langchain invocation with autonomous tool usage loop, feedback, and memory safety."""
    config_context = ""
    if target_url: config_context += f"Target Website: {target_url}\n"
    if git_repo: config_context += f"Git Repository: {git_repo}\n"

    system_prompt = f"""You are a professional AI Assistant.
Role: {role}
Goal: {goal}
Backstory: {backstory}

{config_context}
CRITICAL MISSION: You are an autonomous expert. 
1. DO NOT stop until the task is 100% PROPERLY COMPLETE.
2. After using tools, ALWAYS SELF-VERIFY: "Did I actually solve the user's core problem?"
3. If a tool failed or yielded poor data, search for alternatives immediately.
4. Continuing status: Work in progress.

You have access to 'A to Z' live tools:
- 🕷️ website_scraper, broken_link_finder
- 🔍 seo_analyzer, pagespeed_checker, keyword_researcher
- 📊 inventory_checker, crm_lead_tracker, sales_reporter
- 🧠 sentiment_analyzer, blog_idea_generator, compile_report
- 📱 telegram_alert, whatsapp_alert
- 🌐 web_search, trend_analyzer, news_fetcher, competitor_finder

Final Response Requirement: Only provide your final answer once you have double-checked all tool outputs for accuracy."""

    messages = [
        ("system", system_prompt),
        ("human", task_description)
    ]
    
    collected_tool_results = []  # Track all tool outputs for fallback
    last_response = None
    
    try:
        # Loop up to 7 times for deep 'A to Z' task completion
        for i in range(7): 
            # MEMORY MANAGEMENT: Keep context lean
            if len(messages) > 12:
                messages = [messages[0]] + messages[-10:]

            response = await llm_with_tools.ainvoke(messages)
            last_response = response
            
            if not response.tool_calls:
                # Agent is done — return its text if non-empty, else build summary from tool results
                if response.content and response.content.strip():
                    return response.content
                elif collected_tool_results:
                    logger.info(f"[{role}] Response was empty, returning compiled tool results.")
                    return "📊 Analysis Complete:\n\n" + "\n\n".join(collected_tool_results)
                else:
                    return "✅ Task completed but no output was generated. Please retry."
            
            messages.append(response)
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"].lower()
                args = tool_call["args"]
                
                status_msg = f"🔄 *{role} Ongoing:* Using `{tool_name}` ... (Step {i+1}/7)"
                print(f"[{role}] {status_msg} {args}")
                if status_callback:
                    await status_callback(status_msg)
                
                # Dynamic Tool Selection — handles any parameter variant LLM sends
                if tool_name == "analyze_website_full":
                    result = analyze_website_full.invoke(args)
                elif tool_name == "website_scraper":
                    result = website_scraper.invoke(args)
                elif tool_name == "broken_link_finder":
                    result = broken_link_finder.invoke(args)
                elif tool_name == "seo_analyzer":
                    result = seo_analyzer.invoke(args)
                elif tool_name == "pagespeed_checker":
                    result = pagespeed_checker.invoke(args)
                elif tool_name == "keyword_researcher":
                    result = keyword_researcher.invoke(args)
                elif tool_name == "inventory_checker":
                    result = inventory_checker.invoke(args)
                elif tool_name == "crm_lead_tracker":
                    result = crm_lead_tracker.invoke(args)
                elif tool_name == "sales_reporter":
                    result = sales_reporter.invoke(args)
                elif tool_name == "sentiment_analyzer":
                    result = sentiment_analyzer.invoke(args)
                elif tool_name == "blog_idea_generator":
                    result = blog_idea_generator.invoke(args)
                elif tool_name == "compile_report":
                    result = compile_report.invoke(args)
                elif tool_name == "telegram_alert":
                    result = telegram_alert.invoke(args)
                elif tool_name == "whatsapp_alert":
                    result = whatsapp_alert.invoke(args)
                elif tool_name == "web_search":
                    result = web_search.invoke(args)
                elif tool_name == "trend_analyzer":
                    result = trend_analyzer.invoke(args)
                elif tool_name == "news_fetcher":
                    result = news_fetcher.invoke(args)
                elif tool_name == "competitor_finder":
                    result = competitor_finder.invoke(args)
                elif tool_name == "check_system_logs":
                    result = check_system_logs.invoke(args)
                else:
                    logger.warning(f"[{role}] Unknown tool called: {tool_name} with args: {args}")
                    result = f"Tool '{tool_name}' not found. Available tools: analyze_website_full, seo_analyzer, keyword_researcher, web_search, trend_analyzer, news_fetcher, competitor_finder."
                
                logger.info(f"[{role}] Tool '{tool_name}' returned: {str(result)[:100]}...")
                collected_tool_results.append(f"[{tool_name}]:\n{str(result)}")
                
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call["id"]
                })
        
        logger.info(f"[{role}] Max tool iterations reached.")
        if last_response and last_response.content and last_response.content.strip():
            return last_response.content
        elif collected_tool_results:
            return "📊 Analysis Complete:\n\n" + "\n\n".join(collected_tool_results)
        return "✅ Task completed."
    except Exception as e:
        logger.error(f"[{role}] FATAL ERROR: {e}")
        return f"Agent {role} encountered an error: {str(e)}"

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
    llm = get_llm("tinyllama", 0.7, use_tools=False)
    messages = [("system", f"You are a Jeenora {role_key}."), ("human", user_input)]
    return llm.invoke(messages).content

def _detect_task_type(user_input: str) -> str:
    """Detect what kind of task the user is requesting."""
    text = user_input.lower()
    # URL / website detection
    if any(kw in text for kw in ["http", ".com", ".in", ".org", ".net", "website", "site", "seo", "analyze", "audit", "pagespeed", "broken link", "keyword"]):
        return "seo"
    if any(kw in text for kw in ["inventory", "stock", "dress", "clothes", "fashion", "restock"]):
        return "inventory"
    if any(kw in text for kw in ["lead", "crm", "customer", "follow up", "followup", "unreplied"]):
        return "crm"
    if any(kw in text for kw in ["sales", "revenue", "report", "daily", "weekly", "monthly"]):
        return "sales"
    if any(kw in text for kw in ["competitor", "rival", "competition"]):
        return "competitor"
    if any(kw in text for kw in ["trend", "market", "agri", "agriculture", "farm", "seed"]):
        return "market"
    return "general"

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

    # --- CEO COMPILES FINAL DECISION ---
    if status_callback:
        await status_callback("👑 *CEO Compiling Final Report...* Almost done.")

    ceo_llm = get_llm(ceo_model, ceo_temp, role=ceo_role)

    if specialist_report:
        ceo_synthesis_task = (
            f"You are the CEO. A specialist agent has completed this task and sent you their report.\n\n"
            f"USER REQUEST: {user_input}\n\n"
            f"SPECIALIST REPORT:\n{specialist_report}\n\n"
            f"Your job: Write a concise, professional CEO-level summary. "
            f"Highlight the KEY FINDINGS, 3 action items, and any urgent alerts. "
            f"Be direct and business-focused. Do NOT repeat the full report — synthesize it."
        )
    else:
        # General task — CEO handles standalone
        ceo_synthesis_task = user_input

    final = await invoke_agent(
        ceo_llm, ceo_role, ceo_goal, ceo_back,
        ceo_synthesis_task,
        target_url=ceo_config.get("target_url", ""),
        git_repo=ceo_config.get("git_repo", ""),
        status_callback=None  # suppress status — we already sent it above
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
