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
