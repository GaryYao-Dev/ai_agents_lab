import asyncio
import os
import signal

from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
from dotenv import load_dotenv

load_dotenv(override=True)

HOST_ADDR = os.getenv("HOST_ADDR", "0.0.0.0:50051")


async def main() -> None:
    host = GrpcWorkerAgentRuntimeHost(address=HOST_ADDR)
    host.start()
    print(f"[host] started at {HOST_ADDR}. Press Ctrl+C to stop.")

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except NotImplementedError:
            # add_signal_handler may not be available on some platforms (e.g., Windows)
            pass

    await stop_event.wait()
    await host.stop()
    print("[host] stopped.")


if __name__ == "__main__":
    asyncio.run(main())
