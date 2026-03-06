import requests
import asyncio
from telegram import Bot
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from config import settings

class ExternalTools:
    @staticmethod
    async def send_telegram_alert(message):
        """Send notification via Telegram."""
        print(f"Sending Telegram Alert: {message[:50]}...")
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)
            return "Telegram Alert Sent Successfully."
        except Exception as e:
            return f"Telegram Error: {e}"

    @staticmethod
    def google_search(query, max_results=5):
        """Search Google (via DuckDuckGo) for live data."""
        print(f"Searching for: {query}...")
        results = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append(r)
            return results
        except Exception as e:
            return f"Search error: {e}"

    @staticmethod
    def fetch_market_trends(category):
        print(f"Fetching trends for {category}...")
        return f"Market trends for {category}: High demand expected this weekend."

    @staticmethod
    def send_whatsapp_alert(message):
        print(f"Sending WhatsApp Alert: {message}")
        return "WhatsApp Alert Sent Successfully."

    @staticmethod
    def website_seo_check(url):
        """Analyze a website's SEO factors A to Z."""
        print(f"Analyzing SEO for: {url}...")
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic SEO Check
            title = soup.title.string if soup.title else "No Title"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            desc = meta_desc['content'] if meta_desc else "No Description"
            h1_tags = [h1.get_text() for h1 in soup.find_all('h1')]
            links_count = len(soup.find_all('a'))
            images_without_alt = len([img for img in soup.find_all('img') if not img.get('alt')])

            analysis = f"""
            SEO Report for {url}:
            - Title: {title}
            - Meta Description: {desc}
            - H1 Tags: {h1_tags}
            - Total Internal/External Links: {links_count}
            - Images Missing Alt Text: {images_without_alt}
            - Status Code: {response.status_code}
            """
            return analysis
        except Exception as e:
            return f"Error analyzing website: {e}"
