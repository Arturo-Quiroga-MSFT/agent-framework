# Real Weather Examples with Azure AI

This directory contains examples that use **real weather data** from the OpenWeatherMap API instead of mock data.

## Setup Instructions

### 1. Get Your OpenWeatherMap API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to your API keys section
4. Copy your API key

### 2. Add API Key to .env File

Add the following line to `/Users/arturoquiroga/GITHUB/agent-framework/python/.env`:

```bash
OPENWEATHERMAP_API_KEY=your_api_key_here
```

### 3. Install Required Dependencies

The `aiohttp` package is required for making HTTP requests. It should already be installed, but if not:

```bash
uv pip install aiohttp
```

## Files in This Directory

- **`weather_utils.py`**: Reusable weather utility functions
  - `get_real_weather()`: Get basic current weather
  - `get_real_weather_detailed()`: Get detailed weather with more metrics

- **Example Files**:
  - `azure_ai_basic_real_weather.py`: Basic example with real weather (non-streaming and streaming)
  - `azure_ai_detailed_real_weather.py`: Detailed weather analysis and comparison examples
  - `azure_ai_multiturn_real_weather.py`: Multi-turn conversations and advanced use cases

## Usage Example

```python
from weather_utils import get_real_weather

# Use as a tool in your agent
async with AzureAIAgentClient(async_credential=credential).create_agent(
    name="WeatherAgent",
    instructions="You are a helpful weather agent that provides real weather information.",
    tools=get_real_weather,
) as agent:
    result = await agent.run("What's the weather like in Seattle?")
    print(result)
```

## Running the Examples

```bash
# Make sure you're using the correct virtual environment
source /Users/arturoquiroga/GITHUB/agent-framework/python/.venv/bin/activate

# Run the basic example
python azure_ai_basic_real_weather.py

# Run the detailed weather example
python azure_ai_detailed_real_weather.py

# Run the multi-turn conversation example
python azure_ai_multiturn_real_weather.py
```

## Example Queries You Can Try

**Basic:**
- "What's the weather in Paris?"
- "Compare the weather in New York and Los Angeles"
- "Is it raining in London?"

**Detailed:**
- "Give me a detailed weather report for Tokyo"
- "What's the visibility and wind speed in San Francisco?"

**Multi-turn:**
- "What's the weather in Barcelona?" → "How does that compare to Madrid?"
- "I want to go hiking. Check the weather in Denver." → "What should I pack?"

## API Limits (Free Tier)

- **Calls per day**: 1,000
- **Calls per minute**: 60
- **Cost**: Free

For more information, visit: https://openweathermap.org/price

## Troubleshooting

### Error: OPENWEATHERMAP_API_KEY not set
- Make sure you added the API key to your `.env` file
- Restart your terminal/IDE after adding the key

### Error: Invalid API key
- Double-check your API key is correct
- Note: New API keys may take a few minutes to activate

### Error: City not found
- Try different city name formats:
  - Simple: `"Seattle"`
  - With country: `"Seattle,US"` or `"London,GB"`
  - With state: `"Seattle,WA,US"`

## Weather Data Provided

The weather functions return:
- **Conditions**: Clear, cloudy, rainy, etc.
- **Temperature**: Current temp and "feels like"
- **Humidity**: Percentage
- **Wind**: Speed and direction
- **Pressure**: Atmospheric pressure
- **Visibility**: In meters
- **Cloudiness**: Percentage

## Next Steps

After setting up your API key, you can:
1. Run the example files in this directory
2. Import `weather_utils` in your own agent examples
3. Customize the weather functions for your specific needs
