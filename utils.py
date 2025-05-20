# utils.py
import requests
from bs4 import BeautifulSoup
import random
import time

# Uncomment to use newspaper3k (recommended for better article extraction)
import newspaper
from newspaper import Article
from newspaper.article import ArticleException

def fetch_article_text_from_url(url: str) -> str | None:
    """
    Fetches and extracts the main text content from a given URL.
    Returns the text content or None if fetching fails.
    """
    # First try using newspaper3k (more robust for article extraction)
    try:
        article = Article(url)
        # Configure article object with additional options
        article.config.browser_user_agent = get_random_user_agent()
        article.config.request_timeout = 15
        
        # Download and parse article
        article.download()
        article.parse()
        
        # If we got meaningful content, return it
        if article.text and len(article.text.strip()) > 100:
            return article.text
        
        # If newspaper3k extracted very little text, fall back to BeautifulSoup
        print("Newspaper3k extracted minimal content, trying BeautifulSoup...")
    except ArticleException as e:
        print(f"Newspaper3k extraction error: {e}")
    except Exception as e:
        print(f"Newspaper3k error: {e}")
    
    # Fallback to BeautifulSoup method
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # Add a small delay to avoid appearing as a bot
        time.sleep(1)
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Basic text extraction (can be improved significantly)
        # Try to find main content tags, remove script/style
        for script_or_style in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script_or_style.decompose()

        # Get text from common main content tags
        main_content_tags = soup.find_all(['article', 'main', '.main', '#main', '.post-content', '.entry-content', '.content', '.post', '.article'])
        if main_content_tags:
            text = ' '.join(tag.get_text(" ", strip=True) for tag in main_content_tags)
        else: # Fallback to body if specific main tags not found
            body = soup.find('body')
            if body:
                text = body.get_text(" ", strip=True)
            else:
                return None # No body tag found

        # Clean up excessive whitespace
        text = ' '.join(text.split())
        return text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

def get_random_user_agent() -> str:
    """
    Returns a random user agent string to help avoid detection as a bot.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
    ]
    return random.choice(user_agents) 