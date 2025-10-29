from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from IPython.display import display, Markdown

load_dotenv(override=True)

params = {
    "command": "uv",
    "args": ["run", "./server.py"],
}



def print_dic_recursive(d: dict, indent: int = 0):
    for key, value in d.items():
        print(' ' * indent + str(key) + ": ", end="")
        if isinstance(value, dict):
            print()
            print_dic_recursive(value, indent + 2)
        else:
            print(str(value))

playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}
async def main():
    instructions = """You calculate date differences using the available tools.

When given a date:
1. Get today's date using playwright tools.
2. Calculate the difference using date_diff with today's date and the target date
3. Present the result clearly showing:
   - Today's date and time
   - Target date
   - Difference in years, months, and days

Always use the tool results exactly as returned."""
    request = "1991-01-28"
    model = "gpt-4o-mini"
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as playwright_server:
            agent = Agent(name="date_calculator", instructions=instructions,
                        model=model, mcp_servers=[mcp_server, playwright_server])
            with trace("date_calculator"):
                result = await Runner.run(agent, request)
            print(result.final_output)
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
