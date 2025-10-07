from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)


# def push(text):
#     requests.post(
#         "https://api.pushover.net/1/messages.json",
#         data={
#             "token": os.getenv("PUSHOVER_TOKEN"),
#             "user": os.getenv("PUSHOVER_USER"),
#             "message": text,
#         }
#     )

def store_record(record):
    # Open the file for reading and writing (create if not exists)
    if not os.path.exists("records.json"):
        with open("records.json", "w", encoding="utf-8") as f:
            pass  # create the file if it doesn't exist

    with open("records.json", "r+", encoding="utf-8") as f:
        current_data = f.read()
        if current_data:
            data = json.loads(current_data)
        else:
            data = []
        data.append(record)
        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()


def record_user_details(email, name="Name not provided", notes="not provided"):
    store_record({"type": "user_details", "email": email,
                 "name": name, "notes": notes})
    return {"recorded": "ok"}


def record_unknown_question(question):
    store_record({"type": "unknown_question", "question": question})
    return {"recorded": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
         {"type": "function", "function": record_unknown_question_json}]

# Initialize OpenAI client
openai_api_key = os.getenv('OPEN_ROUTER_API_KEY')
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=openai_api_key)

# Load name, LinkedIn data, and summary


def load_personal_data():
    name = "Gary Yao"

    # Load LinkedIn PDF
    reader = PdfReader("me/CV_Gary Yao.pdf")
    linkedin = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text

    # Load summary
    with open("me/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()

    return name, linkedin, summary


def handle_tool_call(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool", "content": json.dumps(
            result), "tool_call_id": tool_call.id})
    return results


def create_system_prompt(name, summary, linkedin):
    system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

    system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
    system_prompt += f"With this context, please chat with the user, always staying in character as {name}."
    return system_prompt


def chat(message, history):
    name, linkedin, summary = load_personal_data()
    system_prompt_content = create_system_prompt(name, summary, linkedin)

    messages = [{"role": "system", "content": system_prompt_content}
                ] + history + [{"role": "user", "content": message}]
    done = False
    while not done:
        response = openai_client.chat.completions.create(
            model="x-ai/grok-4-fast:free", messages=messages, tools=tools)
        print(f"Response: {response}", flush=True)
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
