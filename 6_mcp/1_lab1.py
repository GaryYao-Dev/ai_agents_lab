
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import os

load_dotenv(override=True)

fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}

playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}


sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
# Ensure the sandbox directory exists to prevent the MCP filesystem server from exiting immediately
os.makedirs(sandbox_path, exist_ok=True)
files_params = {"command": "npx", "args": [
    "-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}


async def main():
    async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
        fetch_tools = await server.list_tools()

    instructions = """
You browse the internet to accomplish your instructions.
You are highly capable at browsing the internet independently to accomplish your task,
including accepting all cookies and clicking 'not now' as
appropriate to get to the content you need. If one website isn't fruitful, try another.
Be persistent until you have solved your assignment,
trying different options and sites as needed.
"""
    tasks = """Find the best flight options for a round-trip flight from Sydney (SYD)
      to Qingdao (TAO) in the period 2025-12-20 to 2026-01-17. 
      The total trip duration is 2 to 3 weeks, and any time in the period is acceptable, 
      but don't consider the time out of the specified range.
      Find only direct flights and consider the cost.
      There are 3 adults and 1 child traveling.
      No airline preferences and the cost is a key factor.
      Cabin class is economy.
      Save your findings in a markdown file named flight_options.md summarizing the best options.
      This is not a conversation, just provide the final output. If there are options, list them all.
      I have find one 
Sydney (SYD)Qingdao (TAO)Thu, Jan 1, 202609:55 – 18:30(Nonstop)
09:55
SYD Sydney Kingsford SmithT1
Capital Airlines
JD480
Airbus A330
Economy class
18:30
TAO Qingdao Jiaodong Intl.

Qingdao (TAO)Sydney (SYD)Wed, Jan 14, 202617:05 – 07:55+1(Nonstop) on https://au.trip.com/flights/ShowFareNext?pagesource=list&triptype=RT&class=Y&quantity=3&childqty=1&babyqty=0&jumptype=GoToNextJournay&dcity=syd&acity=tao&aairport=tao&ddate=2026-01-01&dcityName=Sydney&acityName=Qingdao&rdate=2026-01-14&currentseqno=2&criteriaToken=SGP_SGP-ALI_PIDReduce-d53b5c35-a60c-4a3e-88cc-bb6f4c273255%5EList-07ca9742-6875-4ec8-9c5b-894b540c7ebc&shoppingid=SGP_SGP-ALI_PIDReduce-8a33db99-e1ca-410f-a6ed-d9673789fcad%5EList-b237da0b-82e3-43ef-baa1-7d4c595179c5&groupKey=SGP_SGP-ALI_PIDReduce-8a33db99-e1ca-410f-a6ed-d9673789fcad%5EList-b237da0b-82e3-43ef-baa1-7d4c595179c5&locale=en-AU&curr=AUD
      Find the similar round-trip options from Qingdao (TAO) to Sydney (SYD)."""

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
            agent = Agent(
                name="investigator",
                instructions=instructions,
                model="gpt-5-nano",
                mcp_servers=[mcp_server_files, mcp_server_browser]
            )
            with trace("investigate"):
                result = await Runner.run(agent, tasks)
                print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
