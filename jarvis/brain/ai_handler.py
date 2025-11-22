from datetime import datetime
import re
import random
from config.settings import settings
from services.weather import WeatherService
from services.news import NewsService
from services.web_search import WebSearchService

class AIHandler:
    def __init__(self):
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.web_search = WebSearchService()
        
        # Simple response patterns for free AI
        self.responses = {
            'greeting': ["Hello! How can I help you?", "Hi there! What can I do for you?", "Hey! I'm here to assist you."],
            'thanks': ["You're welcome!", "Happy to help!", "Anytime!"],
            'goodbye': ["Goodbye! Have a great day!", "See you later!", "Take care!"],
            'unknown': ["I'm not sure about that. Could you try rephrasing?", "That's interesting. Can you tell me more?", "I don't have information on that right now."]
        }
    
    def process_command(self, command):
        """Process user command and return appropriate response"""
        command_lower = command.lower()
        
        # Time queries
        if any(word in command_lower for word in ['time', 'what time']):
            return self.get_current_time()
        
        # Weather queries
        elif any(word in command_lower for word in ['weather', 'temperature', 'forecast']):
            city = self.extract_city_from_command(command)
            return self.weather_service.get_weather(city)
        
        # News queries
        elif any(word in command_lower for word in ['news', 'headlines', 'latest news']):
            return self.news_service.get_latest_news()
        
        # Web search
        elif any(word in command_lower for word in ['search', 'look up', 'find']):
            query = self.extract_search_query(command)
            return self.web_search.search(query)
        
        # Simple conversation
        else:
            return self.get_simple_response(command)
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"It's currently {time_str} on {date_str}"
    
    def extract_city_from_command(self, command):
        """Extract city name from weather command"""
        # Simple extraction - look for "in [city]" or "for [city]"
        patterns = [r'in (\w+)', r'for (\w+)', r'weather (\w+)']
        
        for pattern in patterns:
            match = re.search(pattern, command.lower())
            if match:
                return match.group(1).title()
        
        return "London"  # Default city
    
    def extract_search_query(self, command):
        """Extract search query from command"""
        # Remove common command words
        query = re.sub(r'\b(search|look up|find|for|about)\b', '', command.lower())
        return query.strip()
    
    def get_simple_response(self, message):
        """Get simple rule-based response"""
        message_lower = message.lower()
        
        # Greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
            return random.choice(self.responses['greeting'])
        
        # Thanks
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return random.choice(self.responses['thanks'])
        
        # Goodbye
        elif any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'later']):
            return random.choice(self.responses['goodbye'])
        
        # Questions about self
        elif any(word in message_lower for word in ['who are you', 'what are you', 'your name']):
            return "I'm Jarvis, your personal AI assistant. I can help with weather, news, searches, and basic conversations."
        
        # Math calculations
        elif any(word in message_lower for word in ['calculate', 'plus', 'minus', 'times', 'divided']):
            return self.simple_math(message)
        
        # Default response
        else:
            return random.choice(self.responses['unknown'])
    
    def simple_math(self, expression):
        """Handle simple math calculations"""
        try:
            # Replace words with operators
            expr = expression.lower()
            expr = expr.replace('plus', '+').replace('minus', '-')
            expr = expr.replace('times', '*').replace('divided by', '/')
            
            # Extract numbers and operators
            import re
            numbers = re.findall(r'\d+', expr)
            if len(numbers) >= 2:
                if '+' in expr:
                    result = int(numbers[0]) + int(numbers[1])
                elif '-' in expr:
                    result = int(numbers[0]) - int(numbers[1])
                elif '*' in expr:
                    result = int(numbers[0]) * int(numbers[1])
                elif '/' in expr:
                    result = int(numbers[0]) / int(numbers[1])
                else:
                    return "I can help with basic math: addition, subtraction, multiplication, and division."
                
                return f"The answer is {result}"
            
        except Exception:
            pass
        
        return "I can help with simple calculations like '5 plus 3' or '10 minus 2'."