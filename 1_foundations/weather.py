import base64
from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from datetime import datetime


load_dotenv(override=True)


def store_record(record):
    # Open the file for reading and writing (create if not exists)
    if not os.path.exists("weather_records.json"):
        with open("weather_records.json", "w", encoding="utf-8") as f:
            pass  # create the file if it doesn't exist

    with open("weather_records.json", "r+", encoding="utf-8") as f:
        current_data = f.read()
        if current_data:
            data = json.loads(current_data)
        else:
            data = []
        record["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record['timestamp'] = datetime.now().timestamp()
        data.append(record)
        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()


def weather_api_call(function, params_string):
    # Example params: {"location": "Sydney"}
    # This is a tool that calls the weather API, it should be called by the agent with parameters
    api_key = os.getenv("WEATHER_API_KEY")

    response = requests.get(
        f"http://api.weatherapi.com/v1/{function}.json?key={api_key}&{params_string}"
    )
    if response.status_code == 200:
        store_record(response.json())
        return response.json()
    else:
        return {"error": "Unable to retrieve weather data"}


def fetch_weather_icon(file_name, url):
    if not url.startswith("https://"):
        url = f"https://{url}"
    print(f"Fetching weather icon: {file_name} from {url}", flush=True)

    def _check_file_exists(file_name):
        return os.path.exists(os.path.join("./assest/", file_name))
    if _check_file_exists(file_name):
        with open(os.path.join("./assest/", file_name), "rb") as f:
            image_data = f.read()
        b64 = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/png;base64,{b64}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join("./assest/", file_name), "wb") as f:
            f.write(response.content)
        b64 = base64.b64encode(response.content).decode('utf-8')
        return f"data:image/png;base64,{b64}"
    else:
        return None


weather_api_call_json = {
    "name": "weather_api_call",
    "description": "Use this tool to get current weather information. You must provide a 'function' (e.g., 'current', 'forecast') and a 'params_string' (e.g., 'q=London&days=3') as part of the input.",
    "parameters": {
        "type": "object",
        "properties": {
            "function": {
                "type": "string",
                "description": "The weather API function to call (e.g., 'current', 'forecast')"
            },
            "params_string": {
                "type": "string",
                "description": "The query parameters for the API call (e.g., 'q=London&days=3')"
            }
        },
        "required": ["function", "params_string"]
    }
}

fetch_weather_icon_json = {
    "name": "fetch_weather_icon",
    "description": "Use this tool to fetch and store weather icon images locally. \
      You must provide a 'file_name' (e.g., 'sunny.png') and a 'url' (e.g., \
        'cdn.weatherapi.com/weather/64x64/day/113.png') as part of the input.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "The name to save the image file as (e.g., 'sunny.png'), the file name shouldn't contain any other information like the city name, only weather is enough"
            },
            "url": {
                "type": "string",
                "description": "The URL of the weather icon image (e.g., 'cdn.weatherapi.com/weather/64x64/day/113.png')"
            }
        },
        "required": ["file_name", "url"]
    }
}

tools = [{
    "type": "function",
    "function": weather_api_call_json,
},
    #          {
    #     "type": "function",
    #     "function": fetch_weather_icon_json,
    # }
]

# Initialize OpenAI client
openai_api_key = os.getenv('OPEN_ROUTER_API_KEY')
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=openai_api_key)


def handle_tool_call(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}, arguments: {arguments}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool", "content": json.dumps(
            result), "tool_call_id": tool_call.id})
    return results


def load_api_doc():
    with open("./weather_api_summary.json", "r", encoding="utf-8") as f:
        api_doc = f.read()
    return api_doc


def create_system_prompt():
    api_doc = load_api_doc()
    system_prompt = f"""You are a helpful assistant that always answers as a friendly and professional weather bot.
Your answers should be concise and to the point, providing accurate weather information based on the user's queries.

Tool Usage:
- Use the weather_api_call tool to get current weather information when needed.
- Refer to the following API documentation when making calls to the weather API:
{api_doc}

Data Fidelity:
- Before calling the tool, understand the user's question and extract the necessary parameters.
- Due to API limitations on the free plan, forecast data may be limited to a certain number of days.
- Be very careful to check the date and time in the forecast data returned by the tool.
- Only provide information that is directly available from the API response. Do not invent, extrapolate, or make up data.
- If the requested forecast date or specific information is not present in the tool's response, explicitly state that the data is not available due to API limitations. Do not provide fabricated forecasts.

Response Formatting:
- Always include an emoji in front of weather descriptions, e.g., 🌞 Sunny, 🌧️ Rainy, ❄️ Snowy, 🌩️ Stormy, 🌫️ Foggy, 🌬️ Windy, etc.
- For humidity, use 💧; for wind speed, use 🌬️; for max temperature, use 🔴; for min temperature, use 🔵.
- If you are listing multiple days in a forecast, format the data in a table.
"""
    return system_prompt


def chat(message, history):

    system_prompt_content = create_system_prompt()

    messages = [{"role": "system", "content": system_prompt_content}
                ] + history + [{"role": "user", "content": message}]
    done = False
    while not done:
        response = openai_client.chat.completions.create(
            model="x-ai/grok-4-fast:free", messages=messages, tools=tools, temperature=0.2)
        # print(f"Response: {response}", flush=True)
        if response.choices[0].finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_call(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content


if __name__ == "__main__":

    gr.ChatInterface(chat, type="messages").launch()

    # chatbot = gr.Chatbot(render_markdown=True, type="messages")
    # gr.ChatInterface(chat, type="messages", chatbot=chatbot).launch()

    # fetch_weather_icon(
    #     "sunny.png", "cdn.weatherapi.com/weather/64x64/day/113.png")
    # print(weather_api_call("forecast", "q=Canberra,Australia&days=14"))
