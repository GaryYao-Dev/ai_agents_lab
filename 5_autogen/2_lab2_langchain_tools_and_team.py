"""A multi-agent chat interface using Autogen and Gradio with LangChain tools.
  This example demonstrates how to build a chat interface where multiple agents interact,
  utilizing LangChain tools for enhanced capabilities, and an evaluation agent to review responses.
  """

import gradio as gr
import dotenv
from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core import Image as AGImage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool

dotenv.load_dotenv(override=True)

serper = GoogleSerperAPIWrapper()
langchain_serper = Tool(name="internet_search", func=serper.run,
                        description="useful for when you need to search the internet")
autogen_serper = LangChainToolAdapter(langchain_serper)

model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
search_agent = AssistantAgent(
    "search_agent",
    model_client=model_client,
    tools=[autogen_serper],
    system_message="You are a helpful AI research assistant who searches the internet. Incorporate any feedback you receive.",
)

evaluation_agent = AssistantAgent(
    "evaluator",
    model_client=model_client,
    system_message="You are an evaluator for search_agent's result. You provide constructive feedback for search_agent's responses. \
        You should follow the following rules:\
         1. Fully understand the user's request\
         2. Never ask the user for 'APPROVE'.\
         3. If the search_agent is asking for approval, your answer shouldn't quote it as the quoted 'APPROVE' may end the conversation prematurely.\
         4. When you are satisified with the agent's response, respond with 'APPROVE' immmediately without any additional comments.\
         5. The agent's response should always be readable, like if it's listing information, consider use Markdown formatting.\
         6. If the search_agent's response is not satisfactory, provide specific and constructive feedback on how to improve it.",
)

text_termination = TextMentionTermination("APPROVE")

team = RoundRobinGroupChat([search_agent, evaluation_agent],
                           termination_condition=text_termination, max_turns=20)


async def chat(message, main_history, conversation_history):
    user_message = TextMessage(content=message, source="user")

    response = await team.run(task=user_message)
    print(f"Final response from team: {response}")
    print("Messages:")

    # Update main chatbox with user message and final approved result
    search_agent_messages = [
        msg for msg in response.messages if msg.source == "search_agent"]

    updated_main_history = main_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": search_agent_messages[-1].content}
    ]

    # Update conversation chatbox with all agent interactions
    updated_conversation_history = conversation_history.copy()

    for msg in response.messages:
        print(f"{msg.source}:\n{msg.content}\n\n")

        # Format agent messages with their names
        agent_content = f"**{msg.source}:**\n\n{msg.content}"

        # Alternate roles for visual separation
        if msg.source == "search_agent":
            updated_conversation_history.append({
                "role": "assistant",
                "content": agent_content
            })
        else:  # evaluator
            updated_conversation_history.append({
                "role": "user",
                "content": agent_content
            })

    return updated_main_history, updated_conversation_history

with gr.Blocks() as demo:
    gr.Markdown("## Autogen - Team Interaction with Evaluation Agents")
    gr.Markdown("""
    This demo shows a multi-agent system where a search agent and an evaluator agent work together.
    - **Left Chat**: Final approved results (User ↔ Search Agent)
    - **Right Chat**: Behind-the-scenes conversation (Search Agent ↔ Evaluator)
                """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Final Results")
            main_chatbox = gr.Chatbot(
                label="User & Search Agent", type="messages", height=500)

        with gr.Column():
            gr.Markdown("### Agent Conversation")
            conversation_chatbox = gr.Chatbot(
                label="Search Agent ↔ Evaluator", type="messages", height=500)

    message = gr.Textbox(
        show_label=False, placeholder="Type your message here..."
    )

    message_submit = message.submit(
        chat, [message, main_chatbox, conversation_chatbox], [main_chatbox, conversation_chatbox])
    message_submit.then(lambda: gr.update(value=""), None,
                        message, show_progress=False)

    clear_btn = gr.Button("Clear", variant="stop")
    clear_btn.click(lambda: ([], []), None, [main_chatbox,
                    conversation_chatbox], queue=False)

demo.launch(
    server_name="0.0.0.0",
    server_port=8000,
    inbrowser=True
)
