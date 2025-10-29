## Day 1

### Intro to MCP: The USB

#### Introduction to MCP and the Capstone Project

Welcome to the epic finale week of the complete Agentic AI course. This week, we introduce MCP, the Model Context Protocol from Anthropic, and build our flagship capstone project: an equity trading floor.

Throughout this course, we have covered various agent frameworks, including my favorite, the OpenAI Agents SDK, as well as Crew, LangGraph, and most recently, Autogen. This time, we return to MCP, which is not really a framework but a protocol, as we will discuss. This is where everything comes together.

At the end of the week, I will also provide a retrospective overview of the different frameworks we have covered, mention some others we did not cover directly, and bring it all together.

#### A Note for Those Who Skipped Ahead

I have noticed some people have skipped straight to week six, eager to learn about MCP. While it is open for you to do so, I want to emphasize that you may have missed some valuable foundational content, especially from weeks one and two, which prepare you well for this material.

In week one, we covered what it means to connect with different large language models (LLMs) and orchestrate them using tools. We explored various design patterns for agent models and what it means for a model to be autonomous.

In week two, we introduced the OpenAI Agents SDK, which we will use to leverage MCP this week.

If you have skipped ahead, I suggest at least taking a quick look at weeks one and two to gain this foundational knowledge. For those who have completed the entire course so far, we are in great shape.

#### Introducing the Model Context Protocol (MCP) from Anthropic

MCP was first announced late last year but gained significant traction from January through April of this year. Anthropics themselves describe MCP as the "USB-C of Agentic AI." This term has become popular, and we will explain what it means shortly.

I should point out that the AI-generated image often associated with MCP mistakenly shows a USB-A connector, not a USB-C. MCP is decidedly the USB-C of Agentic AI, and that is what we will discover now.

#### Dispelling Misconceptions About MCP

Let me clarify what MCP is not:

- It is not an agent framework.
- It is not about building agents.
- It is not a fundamental change invented by Anthropic that alters how we do things.
- It is not a way to code agents.

So, what is MCP? It is a protocol, a standard, a way to do things consistently and simply. It provides a simple method to integrate your agents with tools, resources, or prompts created by others, enabling easy sharing of such components.

#### Focus on Tools

Primarily, MCP is about tools. This is where the greatest excitement lies. The ability to share resources, such as retrieval-augmented generation (RAG) sources from others, is also popular. Sharing prompts is possible but less widely adopted.

The core idea is to easily share tools so that one person can build a useful tool that performs a helpful function, and others can readily incorporate that tool into their products. This is why MCP is known as the USB-C for AI applications: it emphasizes connectivity and seamless integration of agent applications with external tools.

#### Reasons to Be Excited and Some Caveats

While MCP is exciting, it is important to note some limitations:

- MCP is just the standard or approach for integrating with others' tools; it is not the tools themselves.
- Anthropic has built a few tools, but the excitement is not about these tools.
- For example, the OpenAI Agents SDK already has a massive tools ecosystem, giving access to many tools created by the community.
- It is easy to turn any function into a tool using a decorator in the OpenAI Agents SDK, enabling your agent to use your own tools effortlessly.
- MCP does not help you build your own tools; in fact, it can make that harder.

The real value of MCP is in frictionlessly connecting with other people's tools, immediately accessing descriptions of what the tools do, their parameters, and running them seamlessly.

#### The Growing Ecosystem and Importance of Adoption

Many people have adopted MCP, resulting in thousands of MCP-based tools available for integration. You can quickly search and incorporate diverse capabilities, making your agent more powerful.

Standards can be very exciting when widely adopted. The World Wide Web became successful because people coalesced around HTML as a standard protocol. Similarly, MCP's excitement stems from its adoption, which drives the ecosystem of tools and enables you to easily equip your agents with enhanced functionality.

#### Key Takeaways

- MCP (Model Context Protocol) is a protocol, not a framework, designed to standardize integration of agents with external tools.
- MCP enables easy sharing and use of tools developed by others, enhancing agent capabilities through connectivity.
- MCP is likened to the USB-C of Agentic AI, emphasizing its role in seamless interoperability.
- The excitement around MCP stems from its growing ecosystem and adoption, not from the tools themselves or agent coding changes.

### Understanding MCP Hosts, Clients, and Servers

#### Introduction to MCP Core Concepts

There are three core concepts behind MCP that need to be explained: the MCP host, MCP client, and MCP server.

#### MCP Host

The MCP host is the overall application in which you equip an agent with tools. For example, the host could be Claude Desktop, the software running on your computer that manages Claude, the language model, and lets you chat with Claude. It could also be an agent architecture built using the OpenAI agents SDK that runs agents and tools. This overall application piece of software running the agent framework is known as the MCP host.

#### MCP Client

The MCP client is a small piece of software, similar to a plugin, that runs inside the host. Each MCP client connects one-to-one with an MCP server. For example, if you are running Claude Desktop and using multiple MCP servers, you will have an MCP client running for each of those servers. The MCP client lives within the host and connects to the server.

#### MCP Server

The MCP server is the actual piece of code that provides tools, context, and prompt templates to your agent. Tools are the most exciting aspect, as they equip the agent with extra capabilities. The MCP server runs outside the host.

#### Example: Fetch MCP Server

Fetch is an MCP server capable of searching the internet and fetching web pages. It operates by launching a headless browser, such as headless Chrome, controlled by Microsoft's Playwright to collect and read page contents. This tool is wrapped in an MCP server that you can run locally. You can configure Claude Desktop to run an MCP client that connects to this fetch MCP server, enabling Claude to read web pages live during chat sessions.

In this setup, the fetch MCP server runs on your computer. Claude Desktop connects behind the scenes to the MCP server, which runs the headless browser, collects web pages, and answers questions based on them. This fetch MCP server was used in Autogen last week, demonstrating its practical application.

#### Architecture Diagram Explanation

Imagine a box representing your computer. Inside it, you have a host running, such as Claude Desktop or software built with the OpenAI agents SDK. You may have multiple MCP servers running on your machine, for example, one connecting to the local file system and another providing weather information. Within the host, you have multiple MCP clients, each connecting to one MCP server running on your computer.

You can also have a remote MCP server running on another machine, which you connect to using an MCP client. However, this is quite rare. Although the term "MCP server" might suggest a remote server, most MCP servers run locally on your machine outside the host. You typically download them from a public repository and run them locally.

For example, the fetch MCP server was retrieved from Anthropic's repository but ran locally on our machine. Our host was Autogen, and we wrote code acting as the client connecting to the server running on our computer. While remote MCP servers are possible, they are uncommon and sometimes called hosted or managed MCP servers.

#### Local MCP Server Configurations

The MCP server running on your machine might perform local processing, such as writing files to your file system. Many MCP servers also access internet functionality, like the fetch MCP server running a web browser to browse the internet or MCP servers that check the weather by calling web services. This is the most common configuration.

It is important to distinguish this from the less common case where your MCP client calls a remote MCP server hosted on another machine.

#### Summary on MCP Server Locations

To reiterate, MCP servers mostly run on your local machine. You download and run them locally. This point is emphasized because the terminology can be confusing. When exploring MCP marketplaces, thousands of MCP servers run locally, and it is rare to find ones you can connect to remotely.

#### MCP Server Transport Mechanisms

There are two different transport mechanisms for MCP servers according to the official Anthropic specification:

- **Stdio (Standard Input/Output):** This is the most common approach. The MCP client spawns a separate process on your computer and communicates with it over standard input and output. This is called Stdio and will be used extensively, including when building custom MCP servers.
- **SSE (Server-Sent Events):** This uses an HTTPS connection and streams back results, similar to how language models stream output. SSE is required when connecting to remote hosted or managed MCP servers, as Stdio cannot be used remotely.

For local MCP servers, either Stdio or SSE can be used, but Stdio is the most common. Understanding the difference between host, MCP client, MCP server, and the transport mechanisms (Stdio vs SSE) is essential.

![1761522940718](image/Week6/1761522940718.png)

#### Conclusion and Next Steps

With this understanding of MCP hosts, clients, servers, and their communication methods, it is time to proceed to the lab where you will make use of MCP servers in the OpenAI agents SDK.

#### Key Takeaways

- MCP architecture consists of three core components: MCP host, MCP client, and MCP server.
- MCP hosts are applications running agents equipped with tools, such as Claude Desktop.
- MCP clients run within the host and connect one-to-one with MCP servers, which provide tools and context.
- MCP servers usually run locally on your machine, often communicating via standard input/output (Stdio), with remote servers being less common.

### Using MCP Servers with OpenAI Agents SDK

#### Introduction to Week Six and MCP

Welcome to week six of the course. We begin with an organized file explorer and a lot of work ahead. The first lab starts here. Remember to set the kernel before proceeding, which by now should be familiar.

This week focuses on the Model Context Protocol (MCP) and the OpenAI Agents SDK, which is a favorite tool. Note that the code you see may differ from the lab as it is constantly updated to keep pace with MCP's rapid evolution. If you are new, ensure you pull the latest code using git as per the guides to stay current.

#### MCP Compatibility and Setup for Windows Users

There is an important note for Windows PC users: MCP currently has production issues on Windows and may not work out of the box. While some workarounds exist, they are unreliable. The recommended and reliable solution is to install the Windows Subsystem for Linux (WSL), which allows running a Linux environment on your PC.

Running Cursor connected through WSL enables MCP to function properly. This has been confirmed through extensive testing and student feedback. Unfortunately, there is no reliable alternative at this time.

When setting up WSL, be mindful of whether you are in the Linux home directory or the Windows home directory. Your work should reside in the Linux home directory. Launching WSL via the `ubuntu` command takes you directly to the Linux home directory, which is safer. Detailed instructions are available in the setup guide.

#### Setup Instructions and Mac User Notes

The setup process is straightforward and similar to previous environment setups. Although it may feel repetitive, completing it ensures MCP will work correctly.

Mac users do not need to worry about these Windows-specific issues and are in a good position to proceed without additional setup.

#### Starting with MCP in OpenAI Agents SDK

We begin by importing necessary modules and loading environment secrets. The plan is to use MCP within the OpenAI Agents SDK by creating an MCP client, spawning an MCP server, and then collecting the tools that the server provides.

We start with the `fetch` tool, which is an SMTP server running a headless browser, as discussed previously.

#### Understanding MCP Server Parameters

Everything in MCP servers begins with parameters, which describe the MCP server. These parameters are structured like a dictionary containing the command line instruction to spawn the MCP server.

For example, the `fetch` parameters specify a command that runs a Python process to install and run a package script locally. Many MCP servers follow this pattern of installing and running a Python repository script.

#### Creating an MCP Client and Spawning the Server

Using the OpenAI Agents SDK, creating an MCP client and spawning the server is straightforward. Using a context manager with `MCPServerStdio`, you provide the parameters describing the server.

It is advisable to specify a timeout longer than the default five seconds, such as 30 or 60 seconds, to avoid premature timeouts.

Once the server is running, you can query it for the tools it offers.

#### Example: Fetch Tool and Its Description

The MCP client runs the command to spawn the server as a Python process. It then connects to the server and requests the list of available tools.

In this example, the server returns a tool named `fetch`. This tool fetches a URL from the internet and can optionally extract its contents as markdown.

Interestingly, the tool's description clarifies that although originally it did not have internet access and would refuse requests, it now grants internet access. This description helps language models understand the tool's capabilities and use it properly.

#### Importance of Tool Descriptions for Language Models

The detailed description provided by the makers of the MCP server is crucial. It informs the language model that it now has internet access, which is a change from previous behavior.

This kind of prompt information is valuable because it guides the language model to use the tool correctly without requiring the developer to manually explain the new functionality.

Using the fetch MCP server thus provides this benefit automatically, enhancing the tool's usability behind the scenes.

#### Key Takeaways

- The Model Context Protocol (MCP) is rapidly evolving, requiring users to keep their code updated.
- Windows users may face compatibility issues with MCP and should use Windows Subsystem for Linux (WSL) for reliable operation.
- MCP servers are spawned via command-line parameters describing the server process.
- OpenAI Agents SDK simplifies creating MCP clients, spawning servers, and retrieving available tools.

### Exploring Node

#### Introduction to Node-Based MCP Servers

We are now moving on to explore another MCP server before returning to put the previous one to use. The first MCP server we examined was a Python-based server executed by calling and passing the name of a package available on PyPI, which you could install using pip.

Now, we will use a JavaScript-based MCP server. While Python-based MCP servers typically run using Python, JavaScript-based ones run using server-side JavaScript, which uses something called Node.js. Many of you are probably familiar with Node.js, but if you are not and do not have Node installed on your system, please follow the provided link to ChatGPT's instructions. Installing Node is very simple, and many people already have it installed.

It is important to have a recent version of Node. If you already have Node but an older version, use a version manager such as nvm to upgrade to a recent version. You can verify your Node version by typing `npx --version` in your terminal, ensuring it returns a recent version.

#### Running a Node-Based MCP Server with Playwright

We will now use Node.js to run a Node-based MCP server. This time, the command we use is not `uvicorn` but `npx`. We use npm, the Node package manager, instead of pip. This MCP server is an official Node package.

The MCP server we are using is based on Microsoft's Playwright, which is browser automation software. This is a particularly popular MCP server that runs with Node using Playwright.

You might recall that the fetch MCP server we previously used also utilizes Playwright behind the scenes. However, there is a benefit to using this Node-based MCP server, which will become clear shortly.

Once we specify the parameters, we use the same code structure: we take `MCPServerStdio` as our context manager, pass in the parameters, and remember that the timeout parameter is important. Then, we call `server_tools` to find the tools provided by this server.

When we run this, it calls `npx`, which installs the package and then calls the tools on it. The result is quite impressive.

Unlike the fetch MCP server, which provided only one tool, this Node-based Playwright MCP server offers much more granular control over the browser process. It provides many tools such as closing the browser, resizing the browser window, viewing console messages, uploading files, pressing keys, navigating back and forward, taking screenshots, dragging, clicking, hovering, and selecting.

This level of fine-grained control over the browser window enables us to write agents that can power a browser window, similar to the sidekick we developed in week four.

One of the great advantages of MCP servers is how easy it is to equip your agent with a wide range of tools. You can find tools that interest you and add them in seamlessly. We will now explore another MCP server, which is also JavaScript-based and Node-based.

#### Using a Node-Based MCP Server for File System Access

First, I will quickly get the name of a directory called `sandbox` inside the current directory. If this directory does not already exist on your file system, you may need to create it.

Then, I create parameters for running the MCP server. The command is `npx` again to run Node. I pass in the name of another npm package, which is an Anthropic example MCP server called `server-file-system`. As the name suggests, it provides file system capabilities.

We list its tools again. This Node program spawns the server, connects to it, and requests the available tools. The server responds with tools that allow reading and writing from your local file system, such as reading a file, reading multiple files, creating a directory, listing a directory, and so on.

Importantly, all file system operations are restricted within the sandbox directory path that we specified. This allows you to equip an agent with tools to read and write from your file system while keeping it isolated within a certain directory for security.

#### Key Takeaways

- Node-based MCP servers use server-side JavaScript and require a recent version of Node.js installed.
- The Node package manager (npm) is used to install and run MCP servers in JavaScript, unlike Python's pip.
- Playwright-based MCP servers provide granular control over browser automation, offering many tools such as closing the browser, resizing, taking screenshots, and more.
- MCP servers can be equipped with various tools, such as file system access within a sandboxed directory, enabling agents to interact with local files securely.

### Building an Agent That Uses Multiple MCP Servers

#### Introduction to Agent Using MCP Servers

You might be thinking, all right, I understand that we can create something that spawns a server and tells us about a bunch of tools, but that does not sound very exciting. We want it to actually perform tasks, and that is what we will address now.

We will create a quick example of an agent that uses these tools.

Here are some instructions for our agent:

- Browse the internet to accomplish your instructions.
- You are highly capable of browsing the internet independently to accomplish your task, including accepting cookies.
- Click "Not now" when prompted.
- If one website is not fruitful, try another.
- Be persistent until you have solved your assignment.

This is a clear set of instructions to prepare our server.

We use the same context manager as before, the one we used to collect the names of tools. We pass in the parameters we want, including the timeout. We do this for both of our files: the MCP server that can write to disk, and the Playwright server that can control a browser in a fine-grained way.

We will create an agent called "investigator". We give it the instructions, specify the model (changing it to the latest GPT-4 mini), and pass in a collection of MCP servers. Instead of passing tools directly, we pass MCP servers. The OpenAI agents SDK queries these servers to understand their tools and provide those capabilities to the investigator agent.

This is the extent of the complexity involved in equipping our agents to use these tools.

Once the agent is created, the next step is to set up a trace to track the agent's activity in the UI. Then, we call the runner with the assignment.

The assignment given to our agent is to find a great recipe for banoffee pie and summarize it in Markdown format.

Banoffee pie is a British dessert that, although we Brits are not well known for our cooking, is something we invented and is truly amazing. It is unfortunate that more people do not know about it, so this agent will investigate it on our behalf.

We run the agent, and after a few seconds of processing, it spawns the MCP servers and opens a browser window on the computer. The agent appears to have navigated to BBC Good Food, indicating it understands the British context and is actively searching.

The browser title confirms that it has located a banoffee pie recipe. This is the result of the MCP server running and driving Playwright. Although we do not see all the behind-the-scenes actions, we observe it clicking and navigating.

From a quick look, this appears to be a legitimate version of banoffee pie. Despite my own poor cooking skills, I am confident I can make banoffee pie.

Most importantly, we check our sandbox and preview the file to confirm that the other MCP server was used to write the recipe to disk.

Thus, the agent has used one MCP server to navigate the internet and find the recipe, and another MCP server to write the recipe to disk. Mission accomplished.

Next, we look at the trace in Open IE to see what happened behind the scenes. The trace shows the MCP tools associated with each MCP server. The browser navigate tool was used to navigate the web page, and the file tools performed a read file and then wrote out the banoffee pie recipe.

This trace illustrates the interactions between the tools. It is important to review it to ensure the agent behaves as expected and uses the correct tools appropriately.

#### Exploring MCP Marketplaces

The exciting moment with MCP is when you first see an MCP marketplace. These marketplaces are websites where you can browse all the MCP servers available to equip your agent.

One popular marketplace is MCP itself. Upon launching it, you see a featured list of MCP servers, including the Playwright MCP server we just used. You can view its parameters, tools, and creator information (Microsoft), which indicates legitimacy.

The explore tab allows you to search and filter MCP servers by categories. For example:

- 4000 servers in Research and Data
- 68 in Browser Automation Knowledge and Memory
- 34 in Memory-related tools
- 19 Calendar Managers
- Many in Monitoring and Visualization
- 7344 in Developer Tools

There may be overlap between categories, but this demonstrates the vast selection available to equip your agents.

Another popular marketplace is Glamour. It provides ratings for security, licensing permissiveness, and quality. The methodology for these ratings is documented, which helps in assessing the security of MCP servers.

The volume of servers available is substantial, emphasizing the richness of the ecosystem.

#### Security Considerations for MCP Servers

Security is a significant concern in the community regarding MCP servers. When running an MCP server, it operates on your computer. Authentication methods exist for connecting to remote or hosted MCP servers.

Typically, you run someone else's code on your computer when using MCP servers. This raises valid concerns, but it is important to remember that this is similar to installing open source packages via pip or npm.

You are installing open source code on your computer, which carries inherent risks. Therefore, you must perform due diligence on the tools you use, just as you would with any package installed from PyPI or npm.

If the package is published by reputable organizations like Microsoft or Anthropic, it is likely safe. Otherwise, you should investigate the repository's stars, community activity, feedback, and security reviews to ensure it meets your standards.

MCP servers are only as safe as any code you download and run on your computer. Some MCP servers can be configured to run inside Docker containers, providing additional security controls.

Ultimately, you should always conduct your own security review by researching the publisher, examining the code, and verifying the repository before running an MCP server.

A particular concern arises when non-technologists or end users add MCP servers to cloud desktops. These users may lack the skills to vet packages properly, such as checking GitHub repositories, community engagement, or publisher reputation.

For knowledgeable users like us, we can perform due diligence on open source packages. However, the risk is higher when end users add MCP servers without such expertise.

Marketplaces like Glamour help by providing security ratings and detailed testing information. You can use these ratings as a starting point and choose MCP servers with high security grades.

#### Key Takeaways

- Created an agent capable of using multiple MCP servers to browse the internet and write to disk.
- Demonstrated how to equip an agent with MCP servers using the OpenAI agents SDK.
- Explored MCP marketplaces showcasing thousands of servers across various categories.
- Emphasized the importance of security and due diligence when running MCP servers on local machines.

### MCP Marketplaces & Security Considerations

#### Introduction to MCP Marketplaces

There are several MCP marketplaces available. One notable example is Smithery, which is very popular among users. Many familiar MCP servers are installed across these marketplaces, including Smithery.

In Smithery, you can find servers such as Playwright from Microsoft. You can explore the MSP server itself and see how to run it directly from the command line using NPM. By logging in, you can access parameters and view the tools it offers.

Smithery, like other marketplaces, is quite popular among users.

#### Resources and Blog Posts on MCP Marketplaces

There are several blog posts and resources worth exploring. For example, Huggingface hosts a post featuring a variety of libraries and marketplaces, including the ones we have already seen such as Smithery.

There are many MCP servers to explore. Awesome MCP servers and Cursor provide directories if you want to integrate MCP servers directly into Cursor to enhance your Cursor agent with this functionality and many more.

The official MCP open source project hosted by Anthropic includes several reference servers, such as Fetch, which we have looked at. These are among the most robust servers you can start with, including Klein.

This is a valuable resource to explore with many great marketplaces.

I also found an article on Huggingface that is very well written, accurate, and thoughtful. It discusses what makes MCP exciting, while also providing a reality check to distinguish hype from reality. It is important for people to understand both the genuine excitement and the limitations of MCP.

It is very worthwhile to review these articles and marketplaces to gain a clear understanding of the MCP landscape.

#### Summary of MCP Concepts Covered

Today, we covered a lot of material including MCP hosts, clients, and servers. MCP servers can be written in Python and launched with UV, or in JavaScript through Mpcs. They can also run in other ways, but these are the main two methods.

There are two transport mechanisms for MCP servers: Studio and ZK. Most importantly, MCP servers are exciting because they make it easy and frictionless to connect your agent to many tools developed by people all over the world. There are thousands of such tools to choose from.

#### Looking Ahead

Next time, we will create our own MCP server and client so that we can contribute to this ecosystem.

I look forward to seeing you then.

#### Key Takeaways

- Smithery is a popular MCP marketplace featuring many familiar MCP servers.
- MCP servers can be written in Python or JavaScript and launched using different methods.
- MCP servers enable easy integration of agents with numerous tools developed worldwide.
- Resources like Huggingface and official MCP projects provide valuable directories and insights into MCP marketplaces.

### Day 1 — Summary and external insights

#### Concise Day 1 recap

- MCP is a protocol (not a framework) that standardizes how agents access tools, resources, and prompts — the “USB‑C of Agentic AI.” The value is in easy, interoperable tool sharing and adoption across an ecosystem, not in changing how you write agents.
- MCP architecture: host (e.g., Claude Desktop or an OpenAI Agents SDK app) runs one MCP client per server; servers run locally most of the time and expose tools/resources via a standard API. Common transports are Stdio (local, process I/O) and SSE (remote/hosted).
- In practice for this course, you used three servers:
  - Fetch (Python) via uvx mcp-server-fetch — to fetch web pages.
  - Playwright (Node) via npx @playwright/mcp — granular browser automation.
  - Filesystem (Node) via npx @modelcontextprotocol/server-filesystem `<sandbox>` — constrained file I/O within a sandbox dir.
- With OpenAI Agents SDK, you spawn servers with MCPServerStdio, discover tools (server.list_tools()), and pass servers to the Agent. The “investigator” agent browses to find a Banoffee pie recipe and writes a markdown summary to disk using two different MCP servers.
- Marketplaces (mcp.so, Glama/Smithery, etc.) surface thousands of servers. Treat security seriously: you’re running other people’s code; prefer reputable publishers, review repos, and use sandboxing.

Reference notes from `6_mcp/1_lab1.ipynb`:

- Uses dotenv, Agent/Runner/trace from agents, and MCPServerStdio.
- Ensures a sandbox directory exists before starting the filesystem server.
- Example parameters: {"command": "uvx", "args": ["mcp-server-fetch"]} and {"command": "npx", "args": ["@playwright/mcp@latest"]}.
- Timeout increased to 60s to avoid startup flakiness; if you upgraded the Agents SDK, list_tools may be under server.session.
- Windows users should prefer WSL; Node is required for the Node-based servers (npx available).

### What the wider community says (Hugging Face article highlights)

- Why MCP is surging now: it squarely solves integration — connecting agents to real systems and data — and it’s open, model‑agnostic, and rapidly gaining a network effect (1,000+ community servers early 2025). Many see it becoming a de facto standard for tool access.
- How it works: agents dynamically discover MCP servers and capabilities without hard‑coded connectors; any model or framework can participate. This shifts tool choice from compile‑time wiring to runtime discovery.
- Position in agent stacks: MCP isn’t an agent brain; it powers the Action layer. It complements orchestrators like LangChain/LangGraph/Crew/LlamaIndex. Adapters already exist so MCP servers can appear as framework “tools.”
- Not a silver bullet: consider operational overhead (managing many local/remote servers), security/governance (authN/Z, logging, policy — e.g., MCP Guardian), tool usability/quality of descriptions, and the ecosystem’s maturity/compatibility. Start small, observe, iterate.
- Emerging capabilities and roadmap: remote servers over SSE, OAuth, a registry for discovery/verification, well‑known endpoints, better streaming/statelessness, proactive servers, and improved namespacing.
- New use cases unlocked: multi‑step cross‑system workflows (calendar/email/db/budget), environment‑aware agents (IoT/OS), multi‑agent cooperation via shared tools, personal assistants with local/private data, and enterprise governance with standardized access.

### Practical takeaways for this repo

- Prefer Stdio for local development; consider SSE for remote/hosted servers later.
- Keep server timeouts generous (30–60s) and pre‑create sandbox dirs to avoid exits.
- Treat every MCP server like any third‑party package: verify publisher, review code, prefer signed/official builds, and use directory sandboxes.
- If the OpenAI Agents SDK changes, adjust list_tools calls as noted in the notebook comments.

Sources: `6_mcp/1_lab1.ipynb`; Hugging Face — “What Is MCP, and Why Is Everyone – Suddenly!– Talking About It?”

#### Minimal code: start servers and list tools

```python
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio
import os

load_dotenv(override=True)

# 1) Define server params (Python + Node based)
fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}
playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}

# Filesystem server needs a sandbox path that exists
sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
os.makedirs(sandbox_path, exist_ok=True)
files_params = {
	"command": "npx",
	"args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path],
}

# 2) Launch servers and list available tools
async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
	tools = await server.list_tools()  # If on newer Agents SDK: await server.session.list_tools()
	print("fetch tools:", [t.name for t in getattr(tools, 'tools', tools)])

async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
	tools = await server.list_tools()
	print("playwright tools:", [t.name for t in getattr(tools, 'tools', tools)])

async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as server:
	tools = await server.list_tools()
	print("filesystem tools:", [t.name for t in getattr(tools, 'tools', tools)])
```

#### Compose an agent with two MCP servers and run a task

```python
from agents import Agent, Runner, trace

instructions = """
You browse the internet to accomplish your instructions.
You are highly capable at browsing independently, accepting cookies,
and clicking 'not now' when appropriate. If one website isn't fruitful,
try another. Be persistent until you solve the assignment.
"""

async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
	async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
		agent = Agent(
			name="investigator",
			instructions=instructions,
			model="gpt-4.1-mini",
			mcp_servers=[mcp_server_files, mcp_server_browser],
		)
		with trace("investigate"):
			# Example from the notebook
			result = await Runner.run(
				agent,
				"Find a great recipe for 锅包肉, then you summarize it in markdown to banoffee.md",
			)
			print(result.final_output)
```

## Day 2

### Intro to Week 6 Day 2: Building Your Own MCP Server

#### Introduction to MCP Server and Client

Welcome to day two of week six, where we delve deeper into MCP. Today, we focus on building our own MCP client and MCP server. It is important to note that we are creating our own implementations, not using pre-existing ones such as USB-A of Agent Guy or USB-C of Agentic I.

#### Core Concepts of MCP Architecture

- The **host** refers to the overall application, such as a cloud desktop or an agent architecture.
- The **client** resides inside the host and maintains a one-on-one connection, typically over input/output, to an MCP server.
- The **MCP server** is a separate process running externally, providing tools, contexts, and prompts to MCP clients within the host.

Most discussions focus on tools, although contexts are also briefly used.

#### MCP Architecture Examples

![1761698489308](image/Week6/1761698489308.png)

- **Local MCP Server:** An MCP server running on your computer, connected to an MCP client locally. For example, the file writer used when creating Banoffee Pie.
- **Local Client with Remote Service:** An MCP client on your machine connects to an MCP server on your machine, which then calls out to a remote internet service. Examples include Playwright and Fetch.
- **Hosted or Managed MCP Server:** An MCP client connects remotely to an MCP server running on another machine. This setup typically uses the Server-Sent Events (SSE) transport mechanism, whereas local connections often use standard input/output (stdio) or SSE, with stdio being more common.

#### MCP Server Implementation Details

- MCP servers can be written in Python or JavaScript.
- Common parameters to describe MCP servers include commands to run or MPW (MCP Wrapper).
- MCP servers can also be created using Docker containers, although UX and MPW are the most common methods.

#### Why Build Your Own MCP Server?

The primary reason to build your own MCP server is to **share it** . When you create a tool that others can use with their agents, you describe it in a way that enables integration. This includes working on prompts and the information surrounding your tool.

Additional benefits include:

- Packaging all tools consistently as MCP servers, which is useful when building an agent system that uses multiple MCP servers.
- Gaining a deeper understanding of the underlying plumbing by building the nuts and bolts yourself.

#### Reasons Against Building an MCP Server

If you are building a tool solely for your own use, creating an MCP server may be unnecessary and inefficient. For example, if you have a function you want to equip your large language model (LLM) with, you can simply decorate that function with `@function_tool` and provide it directly to your LLM using the OpenAI agents SDK or the JSON approach from week one.

In this case, the function is called within your current Python process as a tool, avoiding the extra plumbing and scaffolding required to spawn and communicate with a separate MCP server process over standard input/output.

Therefore, MCP servers are not intended for building your own tools for personal use; they are designed for sharing tools.

#### Key Takeaways

- MCP architecture involves a host application, MCP clients, and MCP servers communicating over input/output.
- MCP servers can run locally or remotely, using different transport mechanisms like stdio or SSE.
- Building your own MCP server is beneficial primarily for sharing tools with others and maintaining consistent packaging.
- For personal use, directly decorating functions as tools is simpler than creating an MCP server, which involves additional complexity.

### Wiring Business Logic into Your MCP Server

#### Introduction to MCP Server and Business Logic

We begin by navigating to the week six folder and then to lab two, where we will create our own MCP server and client. While this setup is relatively simple, it is not trivial. The excitement around MCP stems from its simplicity in using other tools, rather than just creating MCP servers.

#### Exploring the Accounts Python Module

Our first step is to examine a Python module named `accounts`. This module contains extensive code for managing your account, including buying and selling shares, maintaining balances, calculating profit and loss, listing transactions, and executing trades based on market prices. This business logic should feel familiar, as it was generated by our agent engineering team in week three.

The code was created by our agent crew and includes comments and type hints. Although I typically write comments and type hints only when necessary, the agent team did a wonderful job here. We are using this code directly, with only minor modifications.

#### Database Integration

I have updated the code slightly to save accounts in a database, separated into a module called `database`. This module uses SQLite in a straightforward manner, allowing reading and writing of accounts as JSON objects. This database module is integrated with `accounts.py`. Apart from these minor changes, the code remains essentially untouched from what our engineering team produced.

#### Using the Accounts Module

Let's proceed with our lab for today. We will start by importing the `accounts` Python module. Once imported, we can call `account.get` with a name to retrieve the account with that ID. For example, my account shows a balance of $9,400, three Amazon shares, and a list of transactions.

I can buy three more shares of Amazon by calling `buy_shares` and providing a reason. For instance, I might say, "I'm going to buy three shares of Amazon because this bookstore website looks promising." After executing this, I now have six Amazon shares in my account.

Additionally, I can call `account.report` to get a detailed report about the account, and `account.list_transactions` to view all transactions. This demonstrates that the code written by our agents is operational and allows us to perform typical account operations such as buying shares and listing transactions.

#### Writing an MCP Server

Creating an MCP server is straightforward. It involves boilerplate code that wraps existing business logic into an MCP server using libraries provided by Anthropic. Let's examine a Python module called `accountsservice`.

The module begins by importing the `FastMCP` class from Anthropic and the business logic module `account`. We then create an MCP server instance named `account_server` using `FastMCP`.

#### Defining MCP Tools

Several functions are defined and decorated with `@mcp.tool`. Each function, such as `get_balance`, includes a descriptive docstring and delegates its operation to the corresponding business logic function. When the MCP server launches, these tools become available for use.

The tools include `get_balance`, `get_holdings`, `buy_shares`, `sell_shares`, and `change_strategy` for modifying the portfolio's strategy. This setup allows the MCP server to expose business logic functionality as callable tools.

#### MCP Resources

In addition to tools, the server defines resources, which are less common but useful. For example, accessing the resource named after an account returns its report, while accessing the resource named after an account's strategy returns that strategy. These resources are accessible via URIs that describe the requested data.

#### Running the MCP Server

At the bottom of the script, when the Python module is executed, it calls the `run` function on the MCP server, specifying the transport mechanism as standard input/output (stdio). This launches the MCP server, imports the business logic, and prepares it to handle the defined tools and resources.

Overall, writing your own MCP server to wrap business logic and launch a server is not difficult. The code is mostly boilerplate, and the server can be quickly put to use.

#### Key Takeaways

- The MCP server simplifies wrapping existing business logic into callable tools and resources.
- The accounts Python module provides comprehensive business logic for managing accounts, shares, and transactions.
- MCP tools are decorated functions that delegate to business logic, enabling easy server functionality.
- Resources in MCP provide access to specific data endpoints, complementing the tool-based interface.

### Creating Client Code to Use Your MCP Server

#### Introduction to MCP Server and Client

In this session, parameters are being set for a custom MCP server that was just written. The command to run is exactly what would be typed at a command line to execute the module.

The command to run the server is as follows:


```python
python account_server.py
```

Running `account_server.py` creates an MCP server, specifically a fast MCP. It calls `run`, and some functions are decorated as MCP tools.

The OpenAI agents SDK context manager is used with `MCPServerStudio`, passing in the parameters, including a timeout. The server's tools are then listed. Running this will create an MCP client, spawn the MCP server, and ask it what tools are offered. The decorated functions should be visible.

#### Listing and Using MCP Tools

After running, the following decorated functions are available as tools:

- get_balance
- get_holdings
- buy_shares
- sell_shares
- change_strategy

These functions are now accessible.

It is not super easy, but it is also not too difficult. Next, instructions are provided to manage an account for a client and answer questions about the account. For example, the account is under the name Ed, and the balance and holdings are requested.

The latest model is used, and the same code as before is applied. The context manager is used with `MCPServerStudio`, parameters are passed, and the client session timeout is set to 30. Instructions and the model are provided, and the output is displayed.

The server is spawned, tools are called, and the response includes the current cash balance and holdings. For example, the response might state: "Your current cash balance is 8000. Your holdings include six shares of Amazon. If you need any further details, let me know." This demonstrates successfully calling the custom MCP server, which then calls the business logic.

#### Writing an MCP Client

It is not common to write an MCP client anymore. Previously, when working with the OpenAI agents SDK, MCP was not natively supported, so a custom client had to be written and the tools provided to the SDK. However, after an update to the OpenAI SDK, this process was greatly simplified, making previous code obsolete.

With the context manager construct, the OpenAI SDK now automatically creates the client. However, it is still useful to see how to make a client, especially if working with resources rather than tools.

#### The Accounts MCP Client Module

The MCP client is implemented in a Python module called `accounts_clients`. At the top, parameters are specified for launching the MCP server. While this could be made configurable for a generic client, it is currently fixed for the accounts MCP server.

The client needs to:

- List the tools
- Call a tool
- Read resources

The first function lists tools by managing a session, initializing it, calling `list_tools` on the session, and returning the tools. This is necessary for contacting the server and listing its tools.

The second function demonstrates calling a tool and reading a resource by specifying the resource name. MCP returns tools in a format similar to standard JSON used when calling a tool, but with slight differences. Therefore, mapping between the MCP description and the general JSON description is necessary. A function is provided for this mapping.

All of this functionality is now included in the OpenAI agents SDK, so manual implementation is not required. However, reviewing the code can help in understanding how an MCP client operates.

#### Running the MCP Client

To run the MCP client, import the relevant functions from the module. The `list_account_tools` function spawns the MCP server and retrieves its tools. The MCP tools are then reconstituted as OpenAI function tools, similar to using a decorator. Both the MCP tools and the reconstituted function tools are printed for comparison.

The MCP tools are wrappers that create an MCP client, launch the MCP server, and run the business logic, returning results to the language model. This process is now handled automatically by the OpenAI agents SDK, but understanding the underlying mechanics is beneficial.

#### Using the MCP Client for Resources

Another example uses the `read_accounts_resource_client` function to read a resource called editor. The result is a description of the account. Alternatively, the business logic can be imported and called directly, yielding the same result.

This demonstrates that the business logic is wrapped in an MCP server to be available as a resource. The MCP client exposes that resource, allowing calls through the client or directly. Sharing the resource via the MCP client provides a streamlined way for others to access it without needing to understand the underlying business logic.

#### Exercises and Further Exploration

To practice, create an MCP server that provides the current date as a tool. This allows an OpenAI agent to access the current date for context-aware responses. As a more advanced exercise, build an MCP client to accompany the server, following the approach demonstrated for the accounts client and server.

You can also write a native call to OpenAI, similar to week one, using a tool as JSON. This exposes the mechanics of calling a language model with an MCP client and server. While not required for daily work, it is a valuable exercise for deeper understanding.

It is worth noting that providing the current date as a tool is not particularly useful in practice, as it is better to state the date directly in the prompt. This ensures the model always has access to it without needing to call a tool. For more interesting tools, consider creating a calculator or another operation on two inputs, and then write an MCP server and possibly a client for it.

#### Conclusion

This concludes the overview of creating MCP servers and clients, with emphasis on the server side. Exercises are provided for further exploration and understanding.

#### Key Takeaways

- Running the MCP server and client allows for managing accounts and exposing business logic as tools.
- The OpenAI agents SDK now simplifies MCP client creation, but understanding manual client construction is valuable.
- MCP clients can list tools, call resources, and map MCP tool descriptions to standard JSON.
- Creating custom MCP servers and clients is a useful exercise for understanding the underlying mechanics.
