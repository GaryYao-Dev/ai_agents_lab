from dataclasses import dataclass
from typing import Optional
import os

from dotenv import load_dotenv
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables (e.g., OPENAI_API_KEY, SERPER_API_KEY, OPENAI_MODEL)
load_dotenv(override=True)


@dataclass
class Message:
    content: str


def get_serper_tool() -> LangChainToolAdapter:
    """Create an Autogen tool adapter wrapping LangChain's Google Serper tool.

    Requires SERPER_API_KEY in env.
    """
    serper = GoogleSerperAPIWrapper()
    langchain_serper = Tool(
        name="internet_search",
        func=serper.run,
        description="Useful for when you need to search the internet",
    )
    return LangChainToolAdapter(langchain_serper)


def get_model_client(model: Optional[str] = None) -> OpenAIChatCompletionClient:
    """Return an OpenAI chat model client, defaulting to gpt-4o-mini.

    OPENAI_MODEL env var can override the default.
    Requires OPENAI_API_KEY in env.
    """
    name = model or os.getenv("OPENAI_MODEL", "gpt-5-nano")
    return OpenAIChatCompletionClient(model=name)
