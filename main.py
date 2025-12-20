import feedparser
import schedule
from telegram import Bot
from datetime import datetime
import os
import openai
import asyncio

# Configuration
RSS_FEEDS = [
    'https://news.ycombinator.com/rss',
    'https://thenewstack.io/category/open-source/feed/',
    'https://huggingface.co/blog/feed.xml',
    # The list goes on and on
]

TELEGRAM_BOT_TOKEN = 'Your bot token'
TELEGRAM_USER_ID = 'Your Telegram ID'
OPENROUTER_API_KEY = 'Your OPENROUTER API KEY'
CHECK_INTERVAL = 15  # Check every 15 minutes
LAST_CHECK_FILE = 'last_check.txt'

# Initialize clients
bot = Bot(token=TELEGRAM_BOT_TOKEN)
openrouter_client = openai.OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def get_last_check_time():
    """Retrieve the last check timestamp from the file, creating it if it doesn't exist."""
    if not os.path.exists(LAST_CHECK_FILE):
        print(f"'{LAST_CHECK_FILE}' not found. Creating it with the current time as a baseline.")
        now = datetime.now()
        set_last_check_time(now)
        return now
    with open(LAST_CHECK_FILE, 'r') as f:
        return datetime.fromisoformat(f.read().strip())

def set_last_check_time(timestamp):
    """Save the current timestamp to the file."""
    with open(LAST_CHECK_FILE, 'w') as f:
        f.write(timestamp.isoformat())

async def ask_openrouter_about_headlines(headlines):
    """Ask OpenRouter if headlines are worth sending."""
    prompt = """You are a tech news filter. For each headline below, answer with ONLY 'YES' or 'NO'
    (one per line) indicating if it's important enough to disrupt a busy tech professional.
    Consider importance, novelty, and relevance to tech/startups/AI/science.

# if YES, then the bot will send it to me, if NO, then it is not important.

    Headlines:
    {}
    """.format("\n".join([f"{i+1}. {h['title']}" for i, h in enumerate(headlines)]))

    try:
        print(f"🧠 Consulting OpenRouter about {len(headlines)} headlines...")
        response = openrouter_client.chat.completions.create(
            model="company-name/model-name",  # You can change this to any model available on OpenRouter
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )
        decisions = response.choices[0].message.content.strip().split('\n')
        print("✅ OpenRouter has made its decisions.")
        return [d.strip().upper() == 'YES' for d in decisions]
    except Exception as e:
        print(f"Error consulting OpenRouter: {e}")
        return [True] * len(headlines)  # Default to sending if error

async def check_rss():
    """Check RSS feeds for new articles and filter them through Gemini."""
    last_check = get_last_check_time()
    current_time = datetime.now()
    new_articles = []
    
    for feed_url in RSS_FEEDS:
        print(f"🔍 Checking feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        source_name = feed.feed.title
        for entry in feed.entries:
            pub_date = datetime(*entry.published_parsed[:6]) if 'published_parsed' in entry else current_time
            if pub_date > last_check:
                new_articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'source': source_name
                })
    
    if new_articles:
        print(f"Found {len(new_articles)} new articles. Filtering with OpenRouter...")
        decisions = await ask_openrouter_about_headlines(new_articles)
        for article, should_send in zip(new_articles, decisions):
            if should_send:
                message = f"📰 {article['title']}\n\nSource: {article['source']}\n{article['link']}"
                print(f"➡️ Sending article to Telegram: {article['title']}")
                await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
                await asyncio.sleep(1)  # Add a 1-second delay to avoid flood limits
    else:
        print("No new articles found since last check.")
    
    set_last_check_time(current_time)

async def main():
    """Main async loop."""
    schedule.every(CHECK_INTERVAL).minutes.do(lambda: asyncio.create_task(check_rss()))
    
    print("🚀 RSS AI News Feed started. Checking for new articles...")
    
    # Run the first check immediately
    await check_rss()
    
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting gracefully.")