## Day 1

### Microsoft Autogen 0.5.1: AI Agent Framework Explained for Beginners

#### Introduction to Microsoft Autogen 0.5.1

This week focuses on understanding Autogen concepts, specifically Autogen from Microsoft. The framework is open source and was released with version 0.4 in January. This release was described as a ground-up rewrite, adopting an asynchronous, event-driven architecture to address previous criticisms.

#### Key Features of Autogen 0.4 and Beyond

The new architecture aims to improve:

- Observability: Understanding agent interactions.
- Flexibility, control, and scale.

Autogen 0.4 is a direct replacement for Autogen 0.2, with a very different feel and architecture. The decision was made to use the latest version, which is 0.5.1. This version is not radically different from 0.4, but it is the most current.

#### Documentation Differences

When searching for documentation, it is important to be aware of whether it is for version 0.4+ or for the older 0.2 versions, as they look and feel quite different.

#### The Autogen Community Split

Late last year, the original creator and several co-founders of Autogen left Microsoft and created a fork of Autogen. This fork is managed by this group, with the creator now at Google. The fork is called AG2 (for Autogen Gen 2), also known as Agent OS 2. AG2 started from Autogen 0.2, making it compatible and consistent with the earlier version of Autogen. It has broken off from Autogen 0.4, which Microsoft released after the split.

#### Reasons for the Fork

The stated reason for the fork was to allow for more rapid and flexible development, free from the corporate bureaucracy of Microsoft. However, being under the Microsoft umbrella also brings many benefits. The main Microsoft Autogen is widely used, with many enterprise clients and broad adoption.

#### Community Confusion and PyPI Package Ownership

The situation is complicated by the fact that the AG2 group now controls the Discord chat group originally for Autogen, leading to much of the community discussion being about AG2. Newcomers to the Autogen ecosystem may be confused, as documentation and community resources may refer to either AG2 (based on Autogen 0.2) or the official Microsoft Autogen.

Microsoft has made it clear that they will continue to push forward with Autogen, as seen with the release of version 0.4 and beyond. Meanwhile, the AG2 camp claims to be more flexible and faster, with frequent releases. As of now, AG2 is at version 0.8, suggesting swift progress.

#### PyPI Installation Issues

The AG2 team also controls the official PyPI package for Autogen. If you run `pip install autogen`, you will get AG2, not Microsoft's official Autogen. This is problematic and confusing for new users, especially since one would expect Microsoft to own the official PyPI package for their product.

#### Course Direction and Environment Setup

For this course, the decision has been made to use the Microsoft track of Autogen, which currently has a larger community and more traction. Students should be aware of the split and potential confusion in documentation. The course environment is set up to install the official Microsoft Autogen (currently version 0.5.1), not AG2.

The official Microsoft Autogen will be installed in your environment, and it will likely continue to progress quickly. It is important to be aware of these distinctions as you work with Autogen.

#### Key Takeaways

- Microsoft Autogen 0.5.1 is the latest version, featuring an asynchronous, event-driven architecture for improved observability, flexibility, control, and scale.
- There is a split in the Autogen community: the original creators forked the project to create AG2 (Agent OS 2), which is based on Autogen 0.2 and is now managed independently from Microsoft.
- The PyPI package name 'autogen' now installs AG2, not Microsoft's official Autogen, leading to confusion for new users.
- The course will use the official Microsoft Autogen (currently version 0.5.1), and students should be aware of documentation differences and community split.

### AutoGen vs Other Agent Frameworks: Features & Components Compared

#### Introduction to Autogen

Let's begin by discussing what Autogen actually is. We have reviewed several frameworks so far, and Autogen is the last of these frameworks before we consider MCP, which is not really a framework.

Autogen is a collection of different components all unified under the Autogen umbrella name. The first component is called Autogen Core.

Autogen Core is agnostic to the specific frameworks, agents, or large language models (LLMs) being used. It is a general, generic framework designed for building scalable multi-agent systems. It manages aspects such as messaging between agents, even if they are distributed across different locations. Essentially, it acts as a fabric for agents to run within.

While it shares some similarities with concepts like LangGraph, Autogen Core is much simpler. Fundamentally, it serves as a runtime environment for running agents together.

Next is Autogen Agent Chat, which is quite a mouthful. This framework will be very familiar because it closely resembles the OpenAI Agents SDK and Crew. It provides a lightweight, simple abstraction for assembling LLMs into an agent construct, enabling them to use tools and interact with each other.

Autogen Agent Chat is built on top of Autogen Core. On top of Agent Chat, there are additional offerings such as Studio and Magentic One.

Studio is a low-code, no-code application designed for visually constructing agent systems. Magentic One is a command-line console application that manages and runs an out-of-the-box agent framework.

These components collectively make up the Autogen ecosystem. All of this is open source and managed by Microsoft Research, with contributions from people worldwide.

Unlike Crew and LangChain, which may have commercial motivations influencing their product roadmaps, Autogen is positioned as a Microsoft Research community project. Studio and Magentic One are considered research environments and are not ready for production use, a fact clearly stated in their documentation.

Our primary focus will be on Autogen Core and Autogen Agent Chat, as these are the core parts of the framework. We will not delve deeply into the low-code/no-code Studio application since we are coders, nor will we focus extensively on Magentic One, although it appears to be an interesting tool.

We will concentrate mostly on Autogen Agent Chat because it directly compares with Crew, OpenAI Agents SDK, and the agent interaction components of LangGraph. We will also explore Autogen Core to some extent to spark interest and experimentation, often using Agent Chat alongside it.

#### Core Concepts of Autogen Agent Chat

Let's now discuss the fundamental building blocks of the Autogen framework, particularly focusing on Agent Chat. These concepts will be familiar and straightforward, similar to those we have encountered before.

The first concept is **models** , which are similar to the LLMs we have seen in other platforms. The second is **messages** , a core concept that represents communication between agents or events within an agent's interactions, such as tool calls. Messages can originate from users to models, between agents, or within an agent during tool usage.

The third concept is **agents** , which are entities with a model behind them capable of carrying out a series of tasks on behalf of a user or another agent. Finally, **teams** are groups of agents that interact to achieve a common goal, similar to the Crew framework.

For today's session, we will focus briefly on the first three concepts: models, messages, and agents. We will set up a quick example and incorporate some SQL, which will be useful for some participants.

#### Key Takeaways

- Autogen is a comprehensive open-source framework for building scalable multi-agent systems.
- It consists of Autogen Core, Autogen Agent Chat, Studio, and Magentic One, each serving different roles.
- Autogen Core provides a generic runtime for managing messaging and coordination among distributed agents.

### AutoGen Agent Chat Tutorial: Creating Tools and Database Integration

#### Introduction to Autogen Agent Chat

Welcome to week five, day one of the Autogen Agent Chat tutorial, which is the main part of Autogen. This framework is comparable to other agent SDKs like crew. Much of what we do here will look familiar because it is consistent with crew and the OpenAI agents SDK, particularly the initial step of loading the environment as usual.

#### The Model Concept

The first concept is the model, which is similar to concepts like language models (LM) we have encountered before. It acts as a wrapper around calling a large language model. Here, we import the `OpenAIChatCompletionClient`, which is the wrapper for the language model we will be using, GPT-4 mini.

Creating the model client is straightforward: you simply pass in the name of your model. For example, you can create a client for GPT-4 mini or, alternatively, run a local model like LLaMA 3.2 using the same approach. This flexibility allows you to continue working locally instead of using GPT-4 mini.

#### The Message Concept

The second concept is the message, which is unique to Autogen Agent Chat. You create an object called a text message. For instance, a message might have the content "I'd like to go to London" with the source set as the user.

When you run and print this message, it shows the content and the source, encapsulating the communication from the user to the agent. This simple structure forms the basis for message passing in the framework.

#### The Agent Concept

The third concept is the agent, which is similar to previous frameworks. We import the `AssistantAgent` class, which is the fundamental class used in Autogen Agent Chat.

To create an agent, instantiate `AssistantAgent` with a name, such as "airline agent", provide the model client (the underlying language model), and supply a system message that acts like instructions. For example:

> You are a helpful assistant for an airline. You give short, humorous answers.

You can also specify streaming of results by setting the `model_client_stream` parameter. This creates an agent ready to process messages.

#### Passing Messages to the Agent

To interact with the agent, you call its `on_messages` method, passing a list of messages. For example, passing the message "I'd like to go to London" in a list.

You also pass a `cancellation_token` which signals when the message processing is complete. This method is asynchronous, so you must `await` it.

After processing, you can print the content of the chat message returned by the agent. For example, the agent might respond with a humorous answer about London weather.

#### Example Agent Response

When you pass the message "I'd like to go to London" to the agent configured as a helpful airline assistant, it might respond:

> Great choice. Just remember, if it starts raining, it's not a sign to panic. It's just London welcoming you. Ha!

This demonstrates the agent's ability to generate short, humorous answers as instructed.

#### Integrating Tools: Ticket Price Lookup

Next, we enhance the agent by integrating tools. We create a tool to get ticket prices, arming our agent with the ability to look up ticket prices from a SQLite database.

We start by importing `sqlite3`, deleting any existing tickets database to start fresh, then creating a new database with a table called `cities` containing city names and round-trip prices.

We populate the database with ticket prices for cities such as London, Paris, Rome, Madrid, Barcelona, and Berlin.

#### Defining the Database Query Function

We define a simple query function `get_city_price` that takes a city name as input, connects to the database, runs a `SELECT` statement to retrieve the round-trip price for that city, and returns the result.

While this example is simplified and does not include extensive input validation or security measures, it serves as a toy example to demonstrate tool integration.

#### Testing the Query Function

Testing `get_city_price` with inputs like "London" and "Rome" returns prices such as 299 and 499 respectively, confirming that the database is populated and the query function works correctly.

#### Creating a Smarter Agent with Tool Integration

We create a new assistant agent named "smart agent" using the same model client and system message as before. We add the `get_city_price` function as a tool, enabling the agent to query ticket prices.

We also set the attribute `reflect_on_tool_use` to `True`, which allows the agent to continue processing after receiving tool results, rather than returning immediately. This is typically the desired behavior.

#### Lightweight Tool Integration in Autogen

A notable advantage of Autogen is that you can pass Python functions directly as tools without requiring decorators or wrappers. This contrasts with other frameworks like OpenAI agents SDK or LangChain, which require additional syntax or wrappers.

Autogen uses comments to extract tool descriptions, simplifying the integration process and reducing the learning curve.

#### Using the Smart Agent

We call the `on_messages` method of the smart agent, passing the same message "I'd like to go to London". We print the agent's inner messages, which show the function call to `get_city_price` with the city name "London", the result returned (299), and the final response from the model.

The final response might be:

> A round trip ticket to London will set you back 299. Just remember, the only thing you should pack is your sense of humor, because the weather might require it.

This demonstrates the agent's ability to use tools and generate a humorous, informative answer.

#### Summary

This example highlights how simple it is to write a tool that performs a SQL call to a database and integrate it into an Autogen agent. The framework is quick and straightforward, and after less than ten minutes, you can become proficient at agent chat with tool integration.

#### Key Takeaways

- Autogen Agent Chat provides a lightweight abstraction for interacting with large language models, similar to OpenAI agents SDK.
- The core concepts include the model client, message objects, and the assistant agent.
- Tools can be integrated easily, such as a SQLite database query function, enabling agents to perform dynamic lookups.
- Autogen simplifies tool integration by allowing direct use of Python functions without decorators, enhancing ease of use and reducing the learning curve.
