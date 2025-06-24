# RSS + AI: The based way to get news—no scrolling, only what matters to you.

A huge portion of your life gets wasted scrolling and surfing social media sites, just out of FOMO (Fear Of Missing Out) for some important news. Well, some news is really important to you, but…

- Are all of them? **No.**
- Are the brain-rot posts that you passed by important? **No.**
- Are the mindless comments that you read important? **No.**
- Are the things that made you angry and your day worse worth it? **No.**

You're burning **2.5 hours daily** on social media. That's **912 hours a year**, or **38 days**. Over a 50-year adult life, that's **5.2 years WASTED**.

With RSS + AI, you could save at least half that time—**2.6 years**—for building, learning, or just chilling without the mental junk.

**Just eat the fish, spit the bones.**

---

## How It Works

Welcome to the combination of the future and the past. Welcome to the dope combo of **AI** and **RSS**.

Pull your important news, feed it to an LLM with a nice prompt, and look at the tailored output, just for YOU. No algorithms pushing trash, no endless doomscrolling.

---

## Get Started

1.  **Grab the repo:** Clone it from [GitHub](https://github.com/qusaismael/rss-ai).
2.  **Set it up:** Plug in your API keys and Telegram bot details into `main.py`. Both are free to get.
3.  **Add your feeds:** Toss in your go-to RSS feeds in the configuration section.
4.  **Fire it up:** Run `python main.py` and enjoy the extra time you have now.

### Configuration

The main configuration is at the top of the `main.py` file. Here's what it looks like:

```python
# Configuration
RSS_FEEDS = [
    'https://news.ycombinator.com/rss',
    'https://thenewstack.io/category/open-source/feed/',
    'https://huggingface.co/blog/feed.xml',
    # The list goes on and on
]

TELEGRAM_BOT_TOKEN = 'Your bot token'
TELEGRAM_USER_ID = 'Your Telegram ID'
GEMINI_API_KEY = 'Your GEMINI FREEEEEE KEY'
CHECK_INTERVAL = 15  # Check every 15 minutes
```

### Prompt Customization

You can easily change the prompt inside the `ask_gemini_about_headlines` function in `main.py` to get exactly the kind of filtering you want.

```python
    prompt = """You are a tech news filter. For each headline below, answer with ONLY 'YES' or 'NO' 
    (one per line) indicating if it's important enough to disrupt a busy tech professional.
    Consider importance, novelty, and relevance to tech/startups/AI/science.
    
# if YES, then the bot will send it to me, if NO, then it is not important.

    Headlines:
    {}
    """.format("\n".join([f"{i+1}. {h['title']}" for i, h in enumerate(headlines)]))
```

**Ditch the scroll, skip the noise.** 