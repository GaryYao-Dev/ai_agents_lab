import asyncio
import os
import signal

from dotenv import load_dotenv
from autogen_core import RoutedAgent, message_handler, MessageContext
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from common import Message, get_model_client, get_serper_tool

load_dotenv(override=True)

HOST_ADDRESS = os.getenv("HOST_ADDRESS", "127.0.0.1:50051")
AGENT_TYPE = "searcher"  # registration type and AgentId.type
AGENT_NAME = "searcher"


class SearcherAgent(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = get_model_client()
        self._delegate = AssistantAgent(
            name,
            model_client=model_client,
            tools=[get_serper_tool()],
            reflect_on_tool_use=True,
        )

    @message_handler
    async def on_message(self, message: Message, ctx: MessageContext) -> Message:
        prompt = (
            "Use your tools to research the topic below. Respond with JSON format.\n\n"
            f"Topic: {message.content}"
        )
        text_message = TextMessage(content=prompt, source="user")
        resp = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        return Message(content=resp.chat_message.content)


async def main() -> None:
    worker = GrpcWorkerAgentRuntime(host_address=HOST_ADDRESS)
    await worker.start()

    await SearcherAgent.register(worker, AGENT_TYPE, lambda: SearcherAgent(AGENT_NAME))
    print(
        f"[worker:{AGENT_TYPE}] connected to {HOST_ADDRESS}. Registered as '{AGENT_TYPE}' with key 'default'. Press Ctrl+C to stop."
    )

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except NotImplementedError:
            pass

    await stop_event.wait()
    await worker.stop()
    print(f"[worker:{AGENT_TYPE}] stopped.")


if __name__ == "__main__":
    asyncio.run(main())
