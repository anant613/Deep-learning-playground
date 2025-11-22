# Jarvis AI Assistant

A personalized AI assistant with voice interaction, web services, and automation capabilities.

## Features

- 🎤 **Voice Recognition** - Wake word detection and command processing
- 🗣️ **Text-to-Speech** - Natural voice responses
- 🤖 **AI Conversations** - Powered by OpenAI GPT
- 🌤️ **Weather Updates** - Real-time weather information
- 📰 **News Headlines** - Latest news from multiple sources
- 🔍 **Web Search** - Search the web and get quick answers
- ⏰ **Task Scheduling** - Set reminders and automated tasks
- 🌐 **Web API** - REST API for web interface integration

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```

Edit `.env` with your keys:
- **OpenAI API Key** (required) - Get from https://platform.openai.com/
- **Weather API Key** (optional) - Get from https://openweathermap.org/api
- **News API Key** (optional) - Get from https://newsapi.org/

### 3. Run Jarvis
```bash
python main.py
```

## Voice Commands

- **Wake Word**: "Jarvis" (configurable in settings)
- **Time**: "What time is it?"
- **Weather**: "What's the weather in London?"
- **News**: "Give me the latest news"
- **Search**: "Search for Python tutorials"
- **General**: Any question or conversation

## API Endpoints

- `GET /` - Health check
- `POST /api/command` - Process text command
- `POST /api/speak` - Make Jarvis speak text
- `GET /api/weather/{city}` - Get weather for city
- `GET /api/news` - Get latest news
- `GET /api/search/{query}` - Web search

## Configuration

Edit `config/settings.py` to customize:
- Wake word
- Voice settings (rate, volume)
- API endpoints
- Default locations

## Troubleshooting

### Audio Issues
- Install PyAudio: `pip install pyaudio`
- On Windows, you may need Visual C++ Build Tools
- Alternative: Use `sounddevice` instead of `pyaudio`

### API Errors
- Check your API keys in `.env`
- Ensure internet connection for external services
- OpenAI API key is required for AI responses

### Voice Recognition
- Ensure microphone permissions are granted
- Adjust ambient noise if recognition is poor
- Speak clearly after the wake word

## Project Structure

```
jarvis/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── .env.example        # Environment variables template
├── config/
│   └── settings.py     # Configuration
├── voice/
│   ├── listener.py     # Speech recognition
│   └── speaker.py      # Text-to-speech
├── brain/
│   └── ai_handler.py   # AI processing
├── services/
│   ├── weather.py      # Weather service
│   ├── news.py         # News service
│   └── web_search.py   # Web search
├── automation/
│   └── scheduler.py    # Task scheduling
└── web/
    └── api.py          # REST API
```

## Next Steps

1. **Web Interface** - Create a React/HTML frontend
2. **Database** - Add SQLite for conversation history
3. **Plugins** - Extend with custom modules
4. **Mobile App** - Build companion mobile app
5. **Smart Home** - Add IoT device integration

## License

MIT License - Feel free to customize and extend!