"""
Week 4, Day 4 - LangGraph with Browser Tools and Async Operations

This is the start of an AWESOME project! Really simple and very effective.
Converted from 3_lab3.ipynb notebook.

Asynchronous LangGraph Usage:
- To run a tool:  
  Sync: tool.run(inputs)  
  Async: await tool.arun(inputs)
- To invoke the graph:  
  Sync: graph.invoke(state)  
  Async: await graph.ainvoke(state)
"""

from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
import nest_asyncio
import asyncio
from typing import Annotated, List, Any, Optional, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from IPython.display import Image, display
import gradio as gr
from langgraph.prebuilt import ToolNode, tools_condition
import requests
import os
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
import uuid
import textwrap

# Load environment variables
load_dotenv(override=True)

# Introducing nest_asyncio
# Python async code only allows for one "event loop" processing aynchronous events.
# The `nest_asyncio` library patches this, and is used for special situations, if you need to run a nested event loop.
nest_asyncio.apply()


class State(TypedDict):
    messages: Annotated[List[Any], add_messages]


class BrowserChatbot:
    def __init__(self):
        self.llm_with_tools = None
        self.tools = None
        self.all_tools = None
        self.graph = None
        self.chat_id = str(uuid.uuid4())
        self.memory = MemorySaver()
        self.browser = None
        self.playwright = None
        self.pushover_token = os.getenv("PUSHOVER_TOKEN")
        self.pushover_user = os.getenv("PUSHOVER_USER")
        self.pushover_url = "https://api.pushover.net/1/messages.json"

    def push(self, text: str):
        """Send a push notification to the user"""
        requests.post(self.pushover_url, data={
            "token": self.pushover_token,
            "user": self.pushover_user,
            "message": text
        })

    def create_push_tool(self):
        """Create the push notification tool"""
        return Tool(
            name="send_push_notification",
            func=self.push,
            description="useful for when you want to send a push notification"
        )

    async def setup_browser_tools(self):
        """Setup browser tools - needs to be async"""
        # If you get a NotImplementedError here or later, see the Heads Up in the original notebook
        self.browser = create_async_playwright_browser(
            headless=False)  # headful mode
        toolkit = PlayWrightBrowserToolkit.from_browser(
            async_browser=self.browser)
        self.tools = toolkit.get_tools()
        return self.tools

    def chatbot(self, state: State) -> Dict[str, Any]:
        """The main chatbot node that processes messages"""
        print(f"Chatbot received messages: {state['messages']}")

        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    async def setup_llm_and_graph(self):
        """Setup the LLM and graph with tools"""
        llm = ChatOpenAI(model="gpt-4o-mini")
        self.llm_with_tools = llm.bind_tools(self.all_tools)

        await self.build_graph()

    async def build_graph(self):
        """Build the LangGraph workflow"""
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", ToolNode(tools=self.all_tools))
        graph_builder.add_conditional_edges(
            "chatbot", tools_condition, "tools")
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")

        self.graph = graph_builder.compile(checkpointer=self.memory)

        # Display graph structure (if running in Jupyter)
        try:
            with open("graph.png", "wb") as f:
                f.write(self.graph.get_graph().draw_mermaid_png())
        except:
            print("Graph structure visualization not available outside Jupyter")

    def setup_chat_interface(self):
        """Setup the Gradio chat interface"""
        config = {"configurable": {"thread_id": self.chat_id}}

        async def chat(user_input: str, history):
            result = await self.graph.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config
            )
            return result["messages"][-1].content

        self.demo = gr.ChatInterface(chat, type="messages")
        return self.demo

    async def setup(self):
        """Initialize all components"""
        print("Setting up browser tools...")
        await self.setup_browser_tools()

        # Create push tool and combine all tools
        tool_push = self.create_push_tool()
        self.all_tools = self.tools + [tool_push]

        print("Setting up LLM and graph...")
        await self.setup_llm_and_graph()

    def cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.browser.close())
            except RuntimeError:
                # If no loop is running, do a direct run
                asyncio.run(self.browser.close())

    async def launch_chat(self):
        """Launch the chat interface"""
        print("Setting up chat interface...")
        chat_interface = self.setup_chat_interface()

        print("Launching chat interface...")
        chat_interface.launch()


# Global variables for Gradio
chatbot_instance = BrowserChatbot()


def create_demo():
    """Create a Gradio demo that initializes lazily"""

    async def chat_handler(message, history):
        """Handle chat messages with lazy initialization"""
        global chatbot_instance

        # Initialize if not already done
        if chatbot_instance.graph is None:
            await chatbot_instance.setup()

        config = {"configurable": {"thread_id": chatbot_instance.chat_id}}
        result = await chatbot_instance.graph.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config=config
        )
        return result["messages"][-1].content

    return gr.ChatInterface(
        chat_handler,
        type="messages",
        title="Browser Chatbot with LangGraph",
        description="Chat with an AI assistant that can browse the web and send notifications"
    )


# Create the demo instance that Gradio can find
demo = create_demo()


async def main():
    """Main async function to run the application when called directly"""
    global chatbot_instance

    try:
        await chatbot_instance.setup()
        print("Launching chat interface...")
        demo.launch()
    finally:
        chatbot_instance.cleanup()

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
