import requests
from config.settings import settings

class NewsService:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = settings.NEWS_BASE_URL
    
    def get_latest_news(self, country="us", category="general", limit=3):
        """Get latest news headlines"""
        try:
            if not self.api_key:
                return "I need a News API key to provide news updates. Please add your NewsAPI key."
            
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': country,
                'category': category,
                'apiKey': self.api_key,
                'pageSize': limit
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'ok' or not data['articles']:
                return "No news articles found at the moment."
            
            # Format news headlines
            headlines = []
            for i, article in enumerate(data['articles'][:limit], 1):
                title = article['title']
                source = article['source']['name']
                headlines.append(f"{i}. {title} - {source}")
            
            news_text = "Here are the latest headlines: " + ". ".join(headlines)
            return news_text
            
        except requests.exceptions.RequestException as e:
            print(f"❌ News API error: {e}")
            return "Sorry, I couldn't get the latest news right now."
        except KeyError as e:
            print(f"❌ News data parsing error: {e}")
            return "There was an error processing the news data."
        except Exception as e:
            print(f"❌ News service error: {e}")
            return "There was an error getting the news."