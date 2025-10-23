import asyncio
import os

from dotenv import load_dotenv
from autogen_core import AgentId, RoutedAgent, message_handler, MessageContext
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from common import Message

load_dotenv(override=True)

HOST_ADDRESS = os.getenv("HOST_ADDRESS", "127.0.0.1:50051")
QUERY = os.getenv(
    "QUERY",
    "在小米中国官网mi.com/shop,查找小米17和小米17pro的参数，并做对比分析。",
)


async def main() -> None:
    worker = GrpcWorkerAgentRuntime(host_address=HOST_ADDRESS)
    await worker.start()
    try:
        # Ensure the runtime knows about our custom Message type by registering
        # a tiny local agent whose handler type annotation references Message.
        class _TypeRegistrar(RoutedAgent):
            def __init__(self) -> None:
                super().__init__("type_registrar")

            @message_handler
            async def _on(self, message: Message, ctx: MessageContext) -> Message:
                return message

        # Register but don't use it; this primes the serialization registry.
        await _TypeRegistrar.register(worker, "_type_registrar", lambda: _TypeRegistrar())

        operator_id = AgentId("operator", "default")
        resp = await worker.send_message(Message(QUERY), operator_id)
        print("\n==== Operator Response ====")
        print(resp.content)
        print("===========================\n")
    finally:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
