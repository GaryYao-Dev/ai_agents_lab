import gradio as gr
from dotenv import load_dotenv
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage
from tools import send_ha_notification

load_dotenv(override=True)


model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

agent = AssistantAgent(
    name="airline_agent",
    model_client=model_client,
    system_message="You are a helpful assistant. You give short answers.",
    model_client_stream=True,
    tools=[send_ha_notification],
    reflect_on_tool_use=True,
)


async def chat(message, history):
    userMessage = TextMessage(content=message, source="user")
    response = await agent.on_messages([userMessage], cancellation_token=CancellationToken())
    updated_history = history + [{"role": "user", "content": message},
                                 {"role": "assistant", "content": response.chat_message.content}]
    return updated_history


def reset_chat():
    return [], ""  # empty chat history, empty input box


with gr.Blocks() as demo:
    gr.Markdown("# Autogen Agent Chat Example")

    chatbot = gr.Chatbot(
        label="Autogen Agent Chatbot",
        height=400,
        type="messages"
    )
    message = gr.Textbox(
        show_label=False, placeholder="Type your message here..."
    )
    with gr.Row():
        submit_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear", variant="stop")

    message_submit = message.submit(chat, [message, chatbot], chatbot)
    message_submit.then(lambda: gr.update(value=""), None,
                        message, show_progress=False)

    submit_event = submit_btn.click(chat, [message, chatbot], chatbot)
    submit_event.then(lambda: gr.update(value=""), None,
                      message, show_progress=False)
    clear_btn.click(reset_chat, None, [chatbot, message], queue=False)


demo.launch(
    server_port=8000,
    server_name='0.0.0.0'
)
