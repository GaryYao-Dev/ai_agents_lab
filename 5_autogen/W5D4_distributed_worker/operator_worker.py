import asyncio
import os
import signal

from dotenv import load_dotenv
from autogen_core import RoutedAgent, message_handler, MessageContext, AgentId
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from common import Message, get_model_client

load_dotenv(override=True)

HOST_ADDRESS = os.getenv("HOST_ADDRESS", "127.0.0.1:50051")
AGENT_TYPE = "operator"
AGENT_NAME = "operator"
SEARCHER_ID = AgentId("searcher", "default")


class OperatorAgent(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = get_model_client()
        self._delegate = AssistantAgent(name, model_client=model_client)

    @message_handler
    async def on_message(self, message: Message, ctx: MessageContext) -> Message:
        # 1) Ask the searcher for research
        query = message.content
        search_result = await self.send_message(Message(query), SEARCHER_ID)

        # 2) Analyze and synthesize
        analysis_prompt = (
            "You are an operator that synthesizes search results into a concise answer.\n\
              If the search results include multiple listing information, consider showing them in a markdown bullet list.\n\
              Use a table when comparing.\n\
              Don't ask approval from user, do what you can to provide a complete answer.\n"
            f"Search findings:\n{search_result.content}"
        )
        print(f"[operator] analysis prompt:\n{analysis_prompt}\n")
        text = TextMessage(content=analysis_prompt, source="user")
        resp = await self._delegate.on_messages([text], ctx.cancellation_token)
        return Message(content=resp.chat_message.content)


async def main() -> None:
    worker = GrpcWorkerAgentRuntime(host_address=HOST_ADDRESS)
    await worker.start()

    await OperatorAgent.register(worker, AGENT_TYPE, lambda: OperatorAgent(AGENT_NAME))
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
