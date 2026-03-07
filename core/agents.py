from crewai import Agent
from langchain_community.llms import Ollama
from config import settings
import os

# CrewAI requires this env var (set dummy if not using OpenAI)
os.environ["OPENAI_API_KEY"] = "sk-dummy-not-used"

# Use Local Ollama model - FREE, No API Cost!
llm = Ollama(model="llama3.1:8b")

# 1. THE CEO AGENT
ceo_agent = Agent(
    role='Jeenora Group CEO',
    goal='Ensure overall profit and business growth across Agri, Dress, and CRM segments.',
    backstory='You are the digital CEO of Jeenora. You coordinate between departments and make strategic decisions based on data.',
    llm=llm,
    allow_delegation=True,
    verbose=True
)

# 2. FARMER AGENT (Agriculture)
farmer_agent = Agent(
    role='Farmer Success Manager',
    goal='Increase farmer engagement and drive sales for agricultural products.',
    backstory='Expert in agriculture and rural marketing. Focuses on helping farmers succeed.',
    llm=llm,
    verbose=True
)

# 3. DRESS AGENT (Fashion)
dress_agent = Agent(
    role='Fashion Inventory Strategist',
    goal='Monitor dress sales trends and maintain optimal stock levels.',
    backstory='Fashion retail expert. Knows when to restock and what designs are trending.',
    llm=llm,
    verbose=True
)

# 4. CRM AGENT (Consultancy)
crm_agent = Agent(
    role='Customer Relationship Manager',
    goal='Follow up on consultancy leads and ensure high client conversion.',
    backstory='Communications expert. Professional, polite, and persuasive in managing leads.',
    llm=llm,
    verbose=True
)

# 5. SEO & COMPETITOR ANALYST AGENT
seo_agent = Agent(
    role='SEO & Market Intelligence Expert',
    goal='Analyze jeenora.com and its competitors to define a #1 ranking strategy.',
    backstory='You are a master of search engine algorithms and competitor benchmarking. You identify why others rank higher and how to beat them.',
    llm=llm,
    verbose=True
)

# 6. CUSTOMER SUPPORT AGENT
support_agent = Agent(
    role='Customer Success Assistant',
    goal='Help Jeenora customers with order status, products, and general inquiries politely.',
    backstory='You are a helpful and professional customer service agent. You always strive to solve problems and provide accurate information.',
    llm=llm,
    verbose=True
)
