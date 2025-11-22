import requests
from bs4 import BeautifulSoup
import urllib.parse

class WebSearchService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query, num_results=3):
        """Perform web search and return summarized results"""
        try:
            if not query or len(query.strip()) < 2:
                return "Please provide a search query."
            
            # Use DuckDuckGo for search (no API key required)
            search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results
            results = []
            result_elements = soup.find_all('div', class_='result')
            
            for element in result_elements[:num_results]:
                title_elem = element.find('a', class_='result__a')
                snippet_elem = element.find('div', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    snippet = snippet_elem.get_text().strip()
                    results.append(f"{title}: {snippet}")
            
            if results:
                search_summary = f"Here's what I found about '{query}': " + " | ".join(results[:2])
                return search_summary
            else:
                return f"I couldn't find specific information about '{query}' right now."
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Web search error: {e}")
            return f"Sorry, I couldn't search for '{query}' right now due to network issues."
        except Exception as e:
            print(f"❌ Web search service error: {e}")
            return f"There was an error searching for '{query}'."
    
    def get_quick_answer(self, query):
        """Get a quick answer for simple queries"""
        try:
            # Use DuckDuckGo instant answer API
            api_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
            
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for instant answer
            if data.get('AbstractText'):
                return data['AbstractText']
            elif data.get('Answer'):
                return data['Answer']
            elif data.get('Definition'):
                return data['Definition']
            
            return None
            
        except Exception as e:
            print(f"❌ Quick answer error: {e}")
            return None