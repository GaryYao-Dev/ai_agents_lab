# Courses

## Day 1

### Crew AI Framework: Creating Collaborative AI Agent Teams

#### Introduction to Crew AI Framework

Welcome to week three, Crew Week. This week, we will explore the world of Crew AI. You might find it a bit challenging to adjust your mindset now, especially since you have just become familiar and comfortable with the OpenAI Agents SDK. We have grown accustomed to it and understand it well. Suddenly, there will be changes: new terminology and new constructs.

However, there is much in common between the two, along with some differences. You will quickly come to appreciate Crew AI as well. This pattern will repeat over the next few weeks — getting comfortable with one framework, then moving on to the next, keeping in mind their differences, similarities, unique features, advantages, and disadvantages.

Different projects will suit different frameworks. You may find yourself preferring one over another, which may differ from my preference. The goal is to learn from each experiment. Additionally, our commercial projects will vary, requiring different approaches.

#### Overview of Crew AI Offerings

Crew AI actually refers to several different things. We will revisit this multiple times. Autogen is similar in this respect.

When people mention Crew, they might be referring to:

- **Crew AI Enterprise** : Crew's platform for deploying, running, monitoring, and managing agents through various interfaces. Sometimes called the Crew AI platform or officially branded as Crew AI Enterprise. Their landing page at currycomb (not .com) prominently features this.
- **Crew AI UI Studio** : A low-code/no-code platform for assembling agent interactions. It resembles the addendum tool we examined at the very beginning. It is an elegant end-user tool.
- **Crew AI Framework** : An open source framework described as "orchestrating high performing AI agents with ease and scale." This is the open source framework we will focus on.

We will concentrate on the open source framework because our goal is to build agents ourselves by writing code. We will not use the low-code tooling, nor will we necessarily deploy agents on a paid hosting platform, which is the domain of Crew AI Enterprise.

It is worth noting the differences between these platforms. OpenAI and Anthropic have a clear business model centered on their models, which is their revenue source. For groups like Crew, monetization strategies are important. The open source framework is popular and successful, but monetization is achieved through Crew Enterprise and tooling, which is understandable and reasonable.

However, this means their website often includes upselling efforts to encourage users to adopt the open source toolkit and eventually pay for hosting and deployment within the broader Crew platform.

#### Focus on the Open Source Crew AI Framework

For the remainder of our discussions, we will work exclusively with the open source Crew AI Framework. Within this framework, there are two distinct approaches:

- **Crew** : This approach involves autonomous solutions where teams of agents with different roles collaborate. "Crew" is Crew's term for a team of agents.
- **Flows** : A newer addition to Crew, Flows represent prescribed workflows that divide problems into multiple steps with decision points and outcomes. They are more deterministic and auditable.

Documentation suggests choosing Crew for autonomous problem solving, creative collaboration, or exploratory tasks, and Flows for deterministic outcomes, auditability, or precise control.

It is likely that Flows emerged in response to concerns about running Crews in production, where uncertainty and lack of auditability can be problematic. In such cases, a tightly defined workflow is preferable to a fully autonomous agentic solution.

This context should help you understand the landscape. As expected, our focus will be on Crews, as this course is about building autonomous agents. Building workflows is also possible but is more straightforward and can be done by directly calling language models and interpreting their responses.

Our interest lies in the autonomous aspect — enabling different language models to choose their own paths and solve problems agentically. This will be our focus for the week.

#### Key Takeaways

- Crew AI consists of multiple offerings: Crew AI Enterprise, Crew AI UI Studio, and the open source Crew AI Framework.
- The open source Crew AI Framework focuses on orchestrating high-performing AI agents with ease and scale.
- Crew AI supports two main approaches: Crew (teams of autonomous agents) and Flows (prescribed, deterministic workflows).
- This course emphasizes building autonomous agent teams using the Crew AI Framework rather than low-code tools or hosted platforms.

### Crew AI Framework Explained: Agents, Tasks & Processing Modes Tutorial

#### Introduction to Crew AI Framework

As we begin week two, we will explore the core concepts of Crew AI, which serve as the foundational building blocks to understand how it operates. There are some similarities to previous frameworks, but also new elements to consider.

An agent is essentially the smallest unit of work, an autonomous entity related to a language model (LM). Each agent has an LM underneath it, along with a role, a description of what it does, a goal, and a backstory. Additionally, an agent can have memory and tools. This defines the agent's structure.

A new concept introduced in Crew AI is the task. Unlike previous frameworks, a task is a specific assignment to be carried out. It includes a description, an expected output, and is assigned to an agent. Thus, tasks are distinct from agents, and multiple tasks can be assigned to a single agent.

A crew is a team composed of agents and tasks. It aggregates these two components and can operate in two different processing modes:

- **Sequential mode:** Executes each task in order as laid out.
- **Hierarchical mode:** Uses a manager LM to assign tasks to agents dynamically.

These are the three core concepts to keep in mind: agents, tasks, and crews.

#### Conceptual Overview and Comparison

These concepts are lightweight and somewhat reminiscent of the previous week's framework but are more opinionated and prescriptive than the OpenAI agents SDK. For example, previously, agents only had an instruction, essentially a system prompt, which was unopinionated and flexible.

In Crew AI, an agent has a role, a goal, and a backstory. This structure is more prescriptive in how one primes the LM and constructs the system prompt, although the exact constitution of the system prompt is not immediately visible to the user.

There are ways to set these components using templates, but these are somewhat hidden, especially at the beginner level. When using Crew AI out of the box, you must provide the role, goal, and backstory.

This approach has trade-offs: it encourages good prompting practices by making you think about context and backstory, which are best practices. However, it may be less flexible in situations where a backstory is irrelevant or unwanted.

Debugging can also be more challenging since the system prompt is constructed from these building blocks rather than being directly controlled.

#### Configuration and Code Separation

A useful feature of Crew AI is the ability to define agents and tasks using configuration files, such as YAML. This allows you to separate textual prompts from your code, improving maintainability and clarity.

For example, a YAML file can specify the role, goal, backstory, and LM associated with an agent named "researcher." This separation means prompts are not buried within code but can be managed independently.

While this adds some scaffolding and requires familiarity with YAML, it is a beneficial practice for organizing your project.

In code, you can create an agent by referencing the configuration rather than specifying all fields manually. This approach is lightweight and transparent, with no hidden magic behind the scenes. It clearly separates concerns, allowing prompt development to proceed independently from coding.

#### The `crew.py` Module and Decorators

The most important Python module in Crew AI is `crew.py`, where everything comes together. This module defines your crew and typically includes decorators to manage agents, tasks, and the crew itself.

Key decorators include:

- `@crew_base`: Applied to the class managing your crew.
- `@agent`: Applied to functions to create agents.
- `@task`: Applied to functions to create tasks.
- `@crew`: Applied to the final function that generates the crew instance.

These decorators help organize your code by automatically associating agents and tasks with the crew instance, enabling clear and concise references within your code.

For example, the crew instance can be created with a list of agents and tasks, specifying the processing mode (sequential or hierarchical). The `@agent` decorator ensures that any function decorated as such automatically adds the created agent to the instance's agent list, allowing easy access later.

This structure will become clearer with concrete coding examples, but the main point is that `crew.py` is central to defining your agents, tasks, and crew using decorators.

#### Key Takeaways

- The Crew AI framework introduces three core concepts: agents, tasks, and crews.
- An agent is an autonomous unit with an LM, role, goal, backstory, memory, and tools.
- Tasks are specific assignments with descriptions, expected outputs, and assigned agents.
- A crew is a team of agents and tasks, operating in either sequential or hierarchical processing modes.
- Crew emphasizes a more prescriptive and opinionated structure compared to the OpenAI agents SDK.
- Configuration files like YAML enable separation of prompts and code, enhancing maintainability.
- The `crew.py` module uses decorators to define agents, tasks, and crews, facilitating clear and organized code structure.

### Crew AI & Lite LM: Flexible Framework for Integrating Multiple LLMs

#### Introduction to Lite LM

One of the advantages of Crew is its very flexible and lightweight approach to interacting with underlying language models (LMs).

It uses a framework called Lite LM under the hood, which facilitates interaction with the actual providers and the LMs themselves.

I appreciate Lite LM because it is extremely simple and vanilla. You may know I have a somewhat love-hate relationship with Lang Chain, which comes with a fair amount of structure. Lite LM is almost the opposite extreme, where there is almost nothing there. You can immediately connect with any LM you can imagine.

This simplicity is reflected in how it is used within Crew. Within Crew, you can create an LM by passing in a model name. The naming convention is that it should have the provider's name followed by a slash and then the model name.

For example, you can work with GPT-4 or Mini, with Claude through Anthropic, you can use 3, 5, 3, 7, or whatever you want. Gemini, Flash, Grok with a Q, and you can also use Grok with a K in the same way. If you are running the model locally, such as Olama, you set it up and supply a base URL.

If you want to use Open Router, which itself is an abstraction over other LMs but is an actual running service, this is how you would configure Open Router as an example.

The core idea is to keep it very lightweight and flexible, allowing you to connect and switch between whichever models are running underneath your Crew.

I would argue that in this way, Crew really has an edge over the OpenAI Agents SDK because it is truly flexible and simple, which I love.

#### Crew AI Projects

Before we dive into coding and creating Crews, let's discuss Crew AI projects. In previous weeks, we have been coding within Python notebooks inside Cursor, and occasionally moving to real Python modules. Crew AI does not work that way.

With Crew, you need to work with Python code, and in fact, Crew builds an entire project and directory structure for each of your Crews. It comes with more scaffolding than we are used to, and there is a particular way you need to use it.

The Crew AI framework itself is already installed because I typed the command `tool install crewai`. This means that when you clone the repository, you already have the Crew AI framework available.

When you want to create a new project, or a Crew of your own, you type the command `crewai create crew mycrew` or `myproject` or whatever you want to name it. This creates the project structure.

As a side note, you could also say `crewai create flow myproject` if you want to use the flow idea, which involves more fixed workflows rather than a Crew. However, we will be sticking with Crews.

The command `crewai create crew mycrew` creates a whole directory structure that appears immediately. At the top level, there is a directory named after your project, such as `mycrew` or `myproject`.

Within that directory, there is a subdirectory called `src`, and inside `src` is another directory named after your project again, for example, `mycrew`.

Inside this nested directory, there is a `config` directory where you put your YAML configuration files. By default, there will be an `agents.yaml` and a `tasks.yaml`, which are used to configure your agents and tasks.

There is also a module called `crew.py`. This module is where everything comes together with decorators and is the place where you actually create your Crew.

Additionally, there is a module called `main.py`. This module is where you initiate the run. When you want to run your project, you simply type `crewai run`, which executes `main.py` behind the scenes.

This brings up a good point: when you type `crewai create crew mycrew`, it sets up a Uvicorn project. This is great for us since we are using Uvicorn as well. It makes a project, so you will also see Uvicorn project configuration files in your project directory.

Therefore, we will have these Uvicorn projects within our larger Uvicorn project for the whole course. This will make more sense when you see it in action.

What better time to see it in action than right now? Let's go and give this a try.

#### Key Takeaways

- Crew AI utilizes a flexible, lightweight framework called Lite LM to interact with various language models.
- Lite LM supports connecting to multiple providers and models using a simple naming convention.
- Crew AI projects require a specific directory structure and scaffolding, created via CLI commands.
- The framework integrates with the Uvicorn server for project execution and management.

### Crew AI Tutorial: Setting Up a Debate Project with GPT-4o mini

#### Introduction to Setting Up a Crew Project

In this session, we are in week three, focusing on the crew folder. The folder is initially empty, as we are starting from scratch, which is the preferred approach for some learners. This method aligns with how Crew operates.

#### Opening the Terminal and Creating a Crew Project

To begin, open a command line or terminal. In Crew, this can be done using Control and the tick key on a Mac, or through the View menu and Terminal if using menus. Change the directory to the third directory, then create a new Crew project by running the appropriate command. The project will be named 'debate' for reasons that will become clear.

##### bash Code Sample

```bash
crew i create crew debate
```

Upon creation, Crew asks which model to start with. You can select OpenAI and choose between GPT-4 or mini for cost efficiency. When prompted for a key, simply press enter if you already have a `.env` file, as Crew attempts to build environment files for you. After pressing enter, several files are created.

#### Exploring the Project Structure in Cursor

The files appear in the explorer pane. If a directory contains only one subdirectory, Cursor or VSCode displays it in a simplified manner. To make the structure clearer, you can create an additional directory named 'other'. This adjustment makes both 'debate' and 'other' visible, enhancing clarity.

##### bash Code Sample

```bash
mkdir other
```

#### Reviewing Crew's Scaffolding

Within the 'debate' folder, Crew has created several directories and files as part of its scaffolding. The 'knowledge' folder contains a 'user preference' file, which holds information about the user. This can be modified and serves as background information for the model, though it will not be used in this instance.

#### Understanding the Source Directory Structure

There is a 'source' folder, which contains a subfolder also named 'debate'. This is the most important directory, as it houses the main components of the project. Inside, there is a 'config' directory with two YAML files: 'agents' and 'tasks'. These files contain default example code, which will be revisited shortly.

#### Additional Scaffolding Components

A 'tools' folder is present, containing basic scaffolding that can be expanded later if needed. In the root of the 'debate' folder, there is a module named 'crew.py' and a 'main.py' file. The 'crew.py' module integrates the crew and includes decorators, while 'main.py' serves as the entry point. The two YAML files under 'config' are prepared for building the first crew.

#### Defining Agents and Their Roles in YAML

The next step is to define the YAML configuration for agents and tasks, starting with the 'agents' YAML file. This file initially contains example agents: the researcher and the reporting analyst. These will be replaced with agents suitable for a debate team. Only two agents are needed: one debater (who will argue both for and against the motion) and a judge.

#### Setting Agent Roles, Goals, and Backstories

For the debater agent, set the role as 'a compelling debater.' The goal is to present a clear argument either in favor of or against the motion. The motion is specified using curly braces, allowing it to be templated and defined at runtime, particularly in 'main.py'. The backstory frames the agent as an experienced debater skilled in concise and convincing arguments. This definition applies to both sides of the debate, with tasks distinguishing between them.

#### Defining the Judge Agent

The judge's role is to decide the winner of the debate based on the arguments presented. The goal is to make a decision based purely on the merits of the arguments, without personal bias. The backstory describes the judge as fair and reputable for impartiality. This approach ensures the agent's outputs align with the intended context.

#### The Importance of Backstory in LLMs

Including a backstory in the agent's definition serves as a system prompt, setting the context for the role. Scientifically, since LLMs predict the most likely next token based on input, providing a detailed backstory increases the probability that outputs will be consistent with the desired context. This method leverages patterns observed during training.

#### Specifying the Model for Each Agent

You can specify the model for each agent, such as GPT-4 or mini. By default, OpenAI is assumed if not explicitly stated. This completes the YAML definition of the agents.

#### Key Takeaways

- The tutorial demonstrates how to create a new Crew project in Cursor, including initializing the project and understanding the folder structure.
- The lecture explains the purpose and content of each directory and file generated by Crew's scaffolding.
- The process of defining agents and their roles, goals, and backstories in the agents YAML file is detailed.
- The importance of backstory in influencing LLM outputs and the option to specify the model for each agent is discussed.

### How to Create an AI Debate System Using Crew AI and Multiple LLMs

#### Introduction to Tasks in Crew AI

We now move on to tasks. Here, there is a research task and a reporting task by default. However, we are going to change this and have a few different tasks.

#### Defining the Propose Task

We will have a task called **propose** . This task is about proposing a motion. The description for this task is: you are proposing the motion, and then the motion gets passed in when we do that part. Come up with a clear argument in favor of the motion. Be very convincing.

The expected output is your clear argument in favor of the motion in a concise manner. The agent associated with this task is the debater agent. We also specify an output file for this task, placing it in a subdirectory called `output` and naming it `propose.md`. This completes our proposal task.

#### Defining the Oppose Task

Next, we create another task called **oppose** . This is the debater that is saying no. Instead of proposing, you are in opposition to the motion. Come up with a clear argument against the motion. Be very convincing. The expected output is your clear argument against the motion. This task is also associated with the debater agent and outputs to `oppose.md`.

#### Defining the Decide Task

The final task is called **decide** . It is important to note that you cannot call your tasks the same thing as your agents, or you will have a problem with conflicting names. Sometimes it is better to call this `propose_task` or `oppose_task`, but here we keep it short. For example, we could not call this task `judge`, as that would conflict with the agent named judge.

The description for the decide task is: review the arguments presented by the debaters and decide which side is more convincing. The expected output is your decision on which side is more convincing and why. The output is saved to a folder called `outputs`.

#### Setting Up the Crew Module

The final steps involve setting up `crew.py` and `main.py`. The default module is `crew.py`, which contains some code based on the standard scaffolding. It creates a class with the `crew_base` decorator, naming the class the same as the project, such as `DebateCrew`.

The generated scaffolding code includes many comments and standard code, which can be removed for clarity. The important part is that it brings in the agents' config and the tasks' config from the config folder, setting them as variables for the class. This allows for easy configuration changes.

You can also bring in your own tools. The next step is to set up the agents. Instead of an agent called researcher, we have an agent called debater. The agent decorator tells Crew that this is an agent. The config should be set to debater, and `verbose=True` provides detailed output during execution. Another agent, judge, is also set up similarly.

#### Defining Tasks in the Crew Module

After removing unnecessary comments, we define our tasks using the task decorator. The propose task is defined, and the output file does not need to be specified again since it is already in the config file. The function is kept simple and clean.

The oppose task is defined next, bringing in the config for oppose. The final task is decide, which is also filled in using the config. This results in two agents and three tasks.

#### Creating the Crew Object

Now, we create the crew in the function `crew`, which has the crew decorator. We simply create an instance of crew, populate the agents and tasks, and choose to be sequential rather than hierarchical in our process. Verbose mode is enabled for detailed output.

#### Setting Up the Main Module

The main module is intended to run the crew locally. It is recommended not to add unnecessary logic. When running the crew, this is where we choose the template values from the YAML file. In this case, we only have one field: motion.

We set the motion to a topic for debate. For example, "There needs to be strict laws to regulate LLMs." This provides a substantial topic for the agents to debate.

#### Running the Crew

After setting up, we are ready to run our first crew. Before running, we make a small change in the main module to print the result to the screen for satisfaction. The result is also saved to a file.

We assign the result of the debate to a variable and print the raw output from the final task sent to the final agent.

Another change is to assign different models to the agents. Instead of both the debater and the judge using OpenAI, we switch the judge to use Claude 3.7 Sonnet latest. This allows Anthropic to judge OpenAI's debates, providing variety.

#### Executing the Debate

To run the debate, open a terminal, change into the crew and debate directories, and type `crew run` to start. The first run may build the environment, but subsequent runs execute immediately. The agents perform their tasks, and the judge decides the winner based on the arguments.

The output shows the arguments in favor and against the motion, and the judge's decision. The output directory contains files with the arguments and the decision, which can be reviewed for further analysis.

#### Summary and Next Steps

We set up the YAML files, the crew module, and the main.py where the motion is set. The debate is run by passing the inputs dictionary with the templated keys and their values. This completes our first experiment with Crew AI. You are encouraged to try this yourself, either by running the provided debates project or by creating a new one.

#### Key Takeaways

- Defined and configured three main tasks for the AI debate system: propose, oppose, and decide.
- Associated tasks with agents and specified output files for each task.
- Explained the importance of avoiding naming conflicts between tasks and agents.
- Demonstrated how to set up and clean the crew and main modules for a streamlined workflow.
- Showed how to run the debate system and interpret the outputs generated by different agents.

### Building AI Debate Systems with CrewAI: Compare Different LLMs

#### Recap of CrewAI Project Setup

We have just experienced a CrewAI project, which is in fact a UV project under the hood. We created it by executing the command `crewai create crew debate`. This action generated a directory structure that should now be available to you.

The directory structure includes folders such as `debate_census`, then `debate` again, followed by `config`. Within these, we set up our `agents.yaml` file to define each of the agents, including their respective models.

We also configured the tasks, which included the expected output and the output file. The `crew` directory contains various decorators, and we brought everything together with our functions for agents, tasks, and the crew itself. We specified that the process was sequential.

By typing `query run` within our directory, the entire process was initiated, generating the output successfully. For example, one output was: "Apparently there should be stricter regulation around LLMs."

#### Encouragement to Experiment

I encourage you to try debating more controversial points of your choice and to select different models for the agents. This will deepen your understanding and provide varied perspectives.

You could create separate agents for the proposer and the opposer of the motion. By breaking them into two different agents and assigning tasks to them separately, it becomes easy to use different models for each role.

For instance, you could have OpenAI debate with DeepSeek, and then switch which model is opposing and which is proposing to observe whether it changes the outcome.

This approach provides an amusing and entertaining way to pit LLMs against each other to see which are better at forming coherent and persuasive arguments that convince a different model acting as the judge.

Such a setup allows you to create your own little leaderboard based on debating skills.

#### Next Steps

Please take the time to enjoy experimenting with this framework. Get a good handle on it and become comfortable with the minimal scaffolding provided by Crew.

In the next session, we will delve deeper into Crew and start building more Crew projects. I look forward to seeing you then.

#### Key Takeaways

- Created a CrewAI project which is essentially a UV project under the hood.
- Set up agents, tasks, and crew configurations to run a debate system.
- Encouraged experimenting with different agents and models to compare debating skills.
- Suggested creating a leaderboard by having models debate and judge each other.

## Day 2

### Building Crew AI Projects: Tools, Context & Google Search Integration

#### Introduction to Crew AI Project Structure

This session continues the exploration of the Crew framework, focusing on building and extending Crew AI projects. The lecture begins with a recap of the foundational elements of Crew AI.

#### Agents, Tasks, and Crews

- An **agent** is the smallest autonomous unit. It typically has a language model (LM) associated with it, though it is not strictly required. Each agent has a role, a goal, a backstory, and can possess memory and tools (not yet explored in detail).
- A **task** is an assignment with a description, expected output, and possibly an output file. It is assigned to an agent. This concept does not have a direct analog in the OpenAI agent SDK.
- A **crew** is a team of agents and tasks assigned to those agents. Crews can operate sequentially or hierarchically. In hierarchical setups, a manager LM determines which task is assigned to which agent.

#### Setting Up a Crew Project: Five Steps

The lecture reviews the five steps required to set up a Crew project:

1. **Create a project:** Use the command to create a new Crew project, which sets up the file system structure.
2. **Navigate to the config:** Enter the `source/<project_name>/config` directory to find the YAML files. By default, there are two YAML files: one for agents and one for tasks. Fill these with the necessary details.
3. **Configure agents, tasks, and crew:** In the `crew.py` module, create agents, tasks, and the crew using the provided functions and decorators. Reference the YAML config files, though it is possible to manually pass in fields when creating objects. The config files help keep prompting text separate from code.
4. **Update Main.py:** Set the config and run parameters, such as specifying the topic or motion for a debate.
5. **Run the project:** Execute the project by running the appropriate command from within the project folder. This initiates the Crew framework.

#### Deepening Understanding: Tools and Context

The session aims to go deeper in two ways while setting up another Crew project:

- **Tools:** Equipping agents with capabilities, following the Crew AI approach.
- **Context:** Defining how information is passed from one task to another within Crew AI.

#### Introducing the Serpa API for Google Search Integration

Before proceeding with Crew, the lecture introduces another API, Serpa, which enables fast Google queries from code. Serpa is a free API that provides lightning-fast Google search capabilities.

- Visit Serpa Dev to sign up and obtain 2,500 free credits, sufficient for the course.
- Generate an API key and copy it to the clipboard for use in the `.env` file.
- Enter the key as `SERPA_API_KEY` in the environment file. The cursor will prompt for this if needed.
- Note: Serp stands for Search Engine Results Page. Ensure you use the correct key, as there are similarly named services.

#### Creating a New Crew Project: Financial Researcher

The lecture proceeds to demonstrate the creation of a new Crew project. The steps are as follows:

#### Step-by-Step: Creating the Project

- Open a new terminal and navigate to the Crew folder for week three.
- Use the command to create a new Crew project named `financial_researcher`, inspired by the default example.
- Choose OpenAI and GPT-4 or GPT-4 Mini as the language model.
- Skip setting up the key if prompted.
- The project scaffolding is created, and the session is ready to begin work on the new project.

#### Key Takeaways

- Reviewed the structure of Crew AI projects, including agents, tasks, and crews.
- Learned the five essential steps to set up a Crew project, from creation to execution.
- Explored how to equip agents with tools and manage context between tasks in Crew AI.
- Introduced the Serpa API for integrating fast Google search capabilities into Crew projects.

### Building Multi-Agent Financial Research Systems with Crew.ai

#### Introduction to Agents in Financial Researcher Project

Let's begin by closing the terminal and navigating into the financial researcher project. Within the source folder, there is a configuration file where we will start our work. Our focus is on defining agents, specifically a researcher agent and an analyst agent.

The researcher agent acts as a senior financial researcher for a specified company. This agent researches company news and potential. The backstory for this agent is that of a seasoned financial researcher with a talent for finding the most relevant information about a company, known for presenting it clearly and concisely. We can specify the language model (LLM) used for this agent and can mix it up as desired.

The analyst agent is a market analyst and report writer focused on a company. This agent analyzes the company and creates a comprehensive, well-structured report that presents insights clearly and engagingly. The analyst is described as meticulous and skilled, with a background in financial analysis and company research. Providing such detailed backstories encourages better prompting and more meaningful outputs from the language model.

#### Defining Tasks for Agents

We define two main tasks: a research task and an analysis task. The research task involves conducting thorough research on the company, focusing on current status, health, historical performance, challenges, opportunities, recent news, future outlook, and potential developments. The findings should be organized in a structured format with clear sections. The expected output is well-defined sections related to the input company, and this task is assigned to the researcher agent.

The analysis task involves analyzing the research findings and creating a comprehensive report. The report should include sections such as an executive summary, information, insights, and market outlook, formatted professionally. The expected output is a polished, professional report representing the research findings. This task is assigned to the analyst agent.

To ensure continuity, the output from the research task is included as part of the context for the analysis task. Crew.ai facilitates this by allowing us to specify context dependencies easily. We include the research task output as context for the analysis task, ensuring that the analyst has access to the researcher's findings.

An output file named `report.md` is specified in the output directory to store the final report generated by the analyst agent.

#### Configuring Agents and Tasks in Crew.ai

In the crew.ai configuration file, we define the agents and tasks using decorators. We create an agent for the researcher with verbose output enabled, and similarly, an agent for the analyst. We then define the research and analysis tasks, linking them appropriately. The process is set to sequential with verbose output enabled to track progress.

#### Main Execution Script

In the main script, we simplify the code to only include a `run` function that executes the researcher crew. Cursor AI assists by recognizing that the input required is a company name, which is templated in the YAML configuration. This input is automatically populated when running the script.

The results from the financial researcher are captured and printed. This streamlined approach leverages the power of cursor AI to reduce manual coding effort.

#### Model Selection and Performance Considerations

Before running the system, we update the models used by the agents to experiment with different options. For the researcher agent, we select the Deep Seek Chat model, a 671 billion parameter model hosted on Deep Sea's servers, which produces comprehensive research but takes approximately 30 seconds per query.

For the analyst agent, we choose the Grok model, a 70 billion parameter Meta model accessible via high-performance inference. This model runs quickly and efficiently, producing the financial report rapidly.

#### Running the Multi-Agent Financial Research System

We open a new terminal, navigate to the project directory, and run the crew command to start the process. The researcher agent is assigned the task of financial researcher for Tesla, with the company parameter automatically set.

The Deep Seek model takes its time to generate detailed research, after which the analyst agent quickly produces a polished financial report on Tesla using the Grok model. This demonstrates the effective collaboration between agents and the flexibility of model selection.

The final financial report on Tesla is generated successfully, showcasing the ease and power of building multi-agent financial research systems with Crew.ai.

#### Key Takeaways

- Defined distinct roles for a senior financial researcher and an analyst agent to enhance multi-agent collaboration.
- Emphasized the importance of detailed backstories in prompts to improve language model outputs.
- Demonstrated task chaining by passing research output as context to the analysis task for continuity.
- Showcased flexibility in selecting different language models for agents to balance performance and speed.

### Enhancing AI Agents with Web Search: Solving the Knowledge Cutoff Problem

#### Enhancing AI Agents with Web Search

The key point to focus on here is that the second agent, which summarized the research report on Tesla, was leveraging the output from the first agent because that output was included in its context. This is how it was able to provide the summary it gave.

You'll note that the information is as of October 2023, which is somewhat disappointing because it does not reflect the most current financial metrics for Q3 2023. This limitation arises because we rely on the context and knowledge cutoff from DeepSeq, which last trained in 2023 and does not have more recent information. While unfortunate, this is something we can now fix.

#### Adding Web Search Capability

To address this, we will add a tool to our AI agent. This is the main plan for this week, and it will be quite straightforward. We start by closing the current view and returning to the Crew module where we define our crew.

We will add another import statement, importing from Crew AI tools. The clever cursor suggests the Serpa dev tool, which is exactly what we want. This tool from Crew AI enables Google lookups using our Serpa dev account. Remember to place your Serpa API key into the .env file.

#### Granting Tool Access to the Researcher Agent

The challenging part is to give the researcher agent the ability to use this tool. We want only the researcher tool to have access to it. This is actually quite simple: we create an instance of the Serpa dev tool and pass it in the tools list for the researcher agent. That's all it takes.

After saving these changes, we can proceed. We might also consider switching to a different model for faster performance. For example, using OpenAI's GPT-4 or GPT-4 mini can speed up the process.

#### Running the Enhanced Agent

Let's open the terminal, navigate to the financial researcher directory within the crew folder, and run the crew command. We expect the agent to perform a Google lookup about Tesla using the Serpa dev tool.

The researcher is in progress, performing multiple searches on the internet with Serpa. We can observe search results mentioning Tesla's latest news today, including references to 2025, which is promising and indicates recent information is being retrieved.

#### Generating the Report

The researcher continues working and then moves on to the report writer, which interacts with Grok. The summary report generated is current as of early 2025 and includes the most recent news about Tesla. It notes that Tesla has not performed as brilliantly as usual in the last few weeks, providing relevant and recent information.

The report is clear and accurate, demonstrating high-quality output. This is the kind of work that would take about ten to fifteen minutes of manual searching, gathering, and synthesizing information into an email. The AI agent has effectively done this work for us.

#### Ease of Building the Infrastructure

Thanks to Crew AI, building this infrastructure was straightforward. With just a few commands and writing plain English objectives in YAML files for our agents and tasks, we enabled the tool to handle all of this seamlessly.

Unlike OpenAI's costs of 2.5 cents per lookup, these searches have been performed using our free credits, costing us nothing.

#### Encouragement to Experiment

I hope you enjoyed this demonstration and have tried it yourself with similar outcomes. Experiment with different models, especially if you are using LLaMA or other free open-source models. Try modifying instructions and backstories to see how they affect performance. Explore other quick agent projects involving searches to become more familiar with Crew AI, which has a lot to offer.

#### Next Steps

Next time, we will take this project further by experimenting with some of the more advanced features of Crew AI. See you then.

#### Key Takeaways

- Integrated the Serpa dev tool into the AI agent to enable real-time web search capabilities.
- Demonstrated how to update the agent's context with recent information beyond the knowledge cutoff.
- Showcased the ease of extending AI agents using Crew AI tools and YAML configurations.
- Encouraged experimentation with different models and instructions to enhance agent performance.

## Day 3

### Building a Crew AI Stock Picker: Multi-Agent System for Investments

#### Introduction to Crew Week Three

Welcome to Crew Week Three, Day Three. It is time for us to build a new project: the stock picker. I am looking forward to showing you this project.

#### Reminder of the Five Steps to Build a Crew Project

From last time, we use Crew by following five steps:

- Use `crew i create crew`.
- Fill in the YAML files.
- Complete the Crew module.
- Update `main.py` to set any inputs for running.
- Call `crew i run`.

#### New Features in This Project

This time, we will go deeper in three new ways:

1. Structured outputs will return, as we looked at them last week.
2. We will use a custom tool in addition to a tool we will use again.
3. We will try out the hierarchical process, allowing Crew to manage which task goes where.

As you will see, we will have a bit of an adventure with that.

#### Setting Up the Project

We are back in Cursor, in the Project Directory three Crew. Let's open this up and bring up a terminal window again. As before, we will go into that directory and create our new project using:

`crew i create crew`

The name of the project is `Stock picker`, a project to create recommendations for investing in the stock market. Please note this is purely for investigatory purposes and should not be used to make any trading decisions.

We will select OpenAI as our provider, choose GPT-4 Mini, and not set up any environment variables. The Crew has been successfully created.

#### Creating Agents

First, open the `stock_picker` project, navigate to `source/config`, and open the `agents.yaml` file. We will create the agents for this project, adding them one at a time to discuss their roles.

#### Trending Company Finder Agent

The first agent is called the Trending Company Finder. It is responsible for looking in the news and finding trending companies in a particular sector. It reads the news and finds 2 to 3 companies that are trending for further analysis. We will use GPT-4 Mini here, but you can substitute whichever model you prefer.

#### Financial Researcher Agent

The next agent is the Financial Researcher. Given details of trending companies, it provides comprehensive analysis. This agent is a financial expert with a proven track record of deeply analyzing hot companies. Again, we will use GPT-4 Mini as the backstory.

#### Stock Picker Agent

The third agent is the Stock Picker. After finding trending companies and researching them, this agent selects the best one for investment, notifies the user, and provides a detailed report. It is a meticulous, skilled financial analyst with a proven track record of equity selection. We will use GPT-4 Mini here as well.

#### Manager Agent

We will add one more agent: a Manager. This manager is a skilled project manager who can delegate tasks to achieve the goal of picking the best company for investment. This is a simple, vanilla description of the agent.

#### Defining Tasks

Now that we have our four agents, it is time to define the tasks. When defining tasks, the trick is to be very clear and simple.

#### Find Trending Companies Task

- **Description:** Find the top trending companies in the news in this sector by searching the latest news.
- Find new companies that you have not found before.
- **Output:** A list of trending companies in that sector.
- **Assigned Agent:** Trending Company Finder.
- **Output File:** `trending_companies.json`.

Note: The output is in JSON format, which will become clear shortly.

#### Research Trending Companies Task

- **Description:** Given a list of trending companies, provide a detailed analysis of each company in a report.
- **Assigned Agent:** Financial Researcher.
- **Context:** The Find Trending Companies task.
- **Output:** A detailed report file.

Note: There is a one-to-one correspondence between tasks and agents at this point.

#### Pick Best Company Task

- **Description:** Analyze research findings, pick the best company for investment, then send a push notification to the user.
- **Additional:** Provide a one-sentence rationale and respond with a detailed report on why you chose this company and which companies were not selected.
- **Assigned Agent:** Stock Picker.
- **Context:** The Research Trending Companies task.

Note: This task introduces the use of a tool for push notifications, which we have used before but is new in Crew.

#### Prompt Design and Consistency

We have now defined our tasks. It is worth noting how the prompts are very instructive and crisp. I have used consistent language, such as "trending companies," across agents and tasks. These small steps help ensure coherent responses. Although it will not be perfectly coherent, it definitely helps. I have experimented with this extensively. In previous versions, inconsistent language between agents and tasks caused less stability. This is a pro tip for you.

#### Key Takeaways

- Created a multi-agent stock picker project using Crew with clear agent roles.
- Defined precise tasks aligned one-to-one with agents to ensure clarity and coherence.
- Emphasized consistent and instructive prompt language to improve response stability.
- Introduced hierarchical process management and custom tools for enhanced project control.

### Implementing Pydantic Outputs in Crew AI: Stock Picker Agent Tutorial

#### Introduction to Structured Outputs in Crew AI

Now it gets interesting. We are going to move to Crew and start building several components. The first step is to use structured outputs. In other words, we will require our different tasks to provide information according to a particular JSON schema. This approach ensures that we receive the information we want from these agents in a robust, controlled manner.

To achieve this, we create classes that are subclasses of `BaseModel`. This method allows us to describe precisely what we want from the agents.

#### Defining the Trending Company Schema

Let's create a class called `TrendingCompany`. This class is a subclass of `BaseModel`. It represents a company in the news attracting attention. We define fields such as `name`, `ticker`, and `reason`, each with descriptive annotations. This schema lays out the information we want to gather and helps guide the agents and tasks to produce the desired output.

#### Organizing Multiple Trending Companies

Next, we define a second class called `TrendingCompanyList`. This class contains a single field `companies`, which is a list of `TrendingCompany` objects. This structure allows one task to return multiple trending companies in an organized manner.

#### Defining the Trending Company Research Schema

Similarly, we create a `TrendingCompanyResearch` schema. This is another subclass of `BaseModel` that represents detailed research on a company. It includes fields such as `name`, `market_position`, `future_outlook`, and `investment_potential`. By specifying these fields and their descriptions, we force the agent to produce structured information conforming to this schema.

We also define a `TrendingCompanyResearchList` class, which contains a list of `TrendingCompanyResearch` objects. This allows the research task to return detailed research results for multiple companies.

It is important to use consistent and clear terminology. Initially, terms like "newsworthy companies" were used, which introduced ambiguity. Using simple, common terms consistently improves reliability.

#### Defining Agents in Crew AI

Now, we define our Crew class called `StockPicker`. We start by creating the `TrendingCompanyFinder` agent. This agent is decorated with the `@agent` decorator and configured to use the `super_dev_tool` to search for trending companies on the internet.

Next, we create the `FinancialResearcher` agent. This agent uses the `sirpa` tool and is configured accordingly. Initially, there was a missing decorator, but after adding `@agent`, it works correctly.

We remove the `sirpa_dev_tool` from the stock picker since it already has all the necessary information and does not require it.

Thus, we have defined three agents: the trending company finder, the financial researcher, and the stock picker.

#### Defining Tasks

We define the first task, which is to find trending companies using the `TrendingCompanyFinder` agent. This task is configured with an output schema of `TrendingCompanyList`, ensuring the output conforms to the structured JSON format we defined earlier.

Similarly, the `ResearchTrendingCompanies` task is configured to produce output conforming to the `TrendingCompanyResearchList` schema. This guarantees that the research results are structured and consistent.

Finally, we add the `BestCompanyPicker` task, which selects the best company. This task is straightforward and serves as a simple conclusion to the task definitions.

#### Creating the Crew

With agents and tasks defined, we now create the crew. We include the three agents in the crew's agent list. Note that there is a fourth agent, the manager, which is handled separately and not included in the general agents list.

The manager agent is created separately with the `allow_delegation` flag set to `True`. This enables the manager to delegate tasks to other agents, similar to the handoff mechanism in the OpenAI agents SDK.

We return the crew from the `def crew` function, specifying the agents, tasks, and setting the process to `hierarchical` rather than `sequential`. This means a language model will determine which agent performs which task. We also enable verbose mode and specify the manager agent for coordination.

An alternative approach is to define the manager as a language model directly, such as GPT-4. However, defining the manager as a separate agent tends to yield better performance and coherence with the mission.

Note that the manager agent uses the full GPT-4 model rather than a smaller variant, which is more costly but helps maintain coherence. You may choose to use a smaller model if preferred.

This concludes the definition of the crew.

#### Key Takeaways

- Utilized Pydantic BaseModel subclasses to enforce structured JSON outputs from agents.
- Defined clear and consistent schemas for trending companies and their research to guide agent responses.
- Created multiple agents with specific roles and linked them to tasks with constrained output schemas.
- Implemented a manager agent with delegation capabilities to coordinate task assignments hierarchically.

### Custom Tool Development for Crew AI: JSON Schema & Push Notifications

#### Introduction

This session focuses on enhancing the Crew AI stock picker project by implementing a main run function, integrating a custom push notification tool, and utilizing structured outputs and hierarchical agent processes.

#### Implementing the Main Run Function

The default template run function is removed and replaced with a simple run. The crew is passed in with the sector set as technology. The current date is not required. The result is obtained by calling Stockpicker kickoff with the inputs, and the results are printed at the end.

#### python Code Sample

```python
result = Stockpicker.kickoff(inputs)
print(result)
```

#### Running the Crew Process

The terminal is opened, and the user navigates to the stock picker folder. The crew process is started by running the appropriate command. The crew process is autonomous and less predictable, as it can involve multiple agents, searching, and analysis. The process may take some time as it works through its tasks.

#### bash Code Sample

```bash
crew run
```

#### Observing the Results

Upon completion, the process recommends a company (e.g., Anthropics), and the decision is saved in the outputs folder. Additional files such as the research list and trending companies list are also generated in JSON format, conforming to the required schema. Structured outputs ensure proper formatting of results.

#### Adding a Custom Push Notification Tool

A new tool is added to the project. In the source folder, under stock picker, there is a tools folder containing a Custom Tool. This tool is renamed to push_tool.py. The custom tool requires a schema definition using a Pydantic object, and an underscore run method that takes the schema as parameters.

#### Defining the Push Notification Input Schema

A class called PushNotificationInput is created as a subclass of BaseModel. The schema includes a single argument, message, which is the message to be sent to the user.

#### python Code Sample

```python
from pydantic import BaseModel

classPushNotificationInput(BaseModel):
    message: str# The message to be sent to the user
```

#### Implementing the Push Notification Tool

The class is renamed to PushNotificationTool. The name is set to "send a push notification" and the description is "This tool is used to send a push notification to the user." The schema for the arguments is set to the previously defined PushNotificationInput. The run method takes the message as input and sends a push notification using the Pushover tool. The Pushover user and token should be set in the environment file.

#### python Code Sample

```python
import os
import requests

classPushNotificationTool:
    name = "send a push notification"
    description = "This tool is used to send a push notification to the user."
    args_schema = PushNotificationInput

def_run(self, message: str):
        user_key = os.getenv("PUSHOVER_USER")
        api_token = os.getenv("PUSHOVER_TOKEN")
        requests.post(
"https://api.pushover.net/1/messages.json",
            data={
"token": api_token,
"user": user_key,
"message": message
            }
        )
return"OK"
```

#### Integrating the Push Notification Tool with the Agent

The push notification tool is imported into the crew.py module. The stock picker agent is given the ability to call the push notification tool. This allows the agent to send push notifications to the user when a recommendation is made.

#### python Code Sample

```python
from tools.push_tool import PushNotificationTool

# Add PushNotificationTool to the stock picker agent's tools
```

#### Running the Enhanced Crew Process

The process is run again, and this time, when a recommendation is made (e.g., Circle), a push notification is sent to the user. The successful delivery of the push notification confirms the integration is working as intended.

#### Recap of Enhancements

Three main improvements were made:

1. Structured outputs were used, requiring tasks to respond in a JSON schema format.
2. The hierarchical process was used instead of a sequential process, allowing for more flexible task assignment among agents.
3. A custom tool was added to send push notifications, and the stock picker agent was equipped with this capability.

These enhancements demonstrate the flexibility and power of the Crew AI agent framework.

#### Conclusion and Next Steps

This concludes the current phase of the stock picker project. Additional features will be added in the following sessions, and the next project, the developer agent, will be introduced soon.

#### Key Takeaways

- Implemented a run function to initiate the crew process for stock picking.
- Introduced a custom push notification tool using a schema and Pushover integration.
- Enabled the stock picker agent to send push notifications to the user.
- Demonstrated the use of structured outputs, hierarchical agent processes, and custom tools in the Crew AI framework.

## Day 4

### Crew AI Memory: Vector Storage & SQL Implementation for AI Agents

#### Introduction to Crew AI Memory

In this session, we continue from our previous stock picker project, adding a few final touches before moving on to a new developer agent project. Before that, let's review the five essential steps involved in building a Crew project:

1. **Create Crew** : Set up your project by creating the crew, including directories and files.
2. **Define YAML Files** : Fill in YAML files to define your agents and tasks.
3. **Configure crew.py** : Create instances using decorators to identify agents and tasks.
4. **Update Main.py** : Configure inputs and template fields.
5. **Run Crew** : Execute the project using Crew.

This overview sets the stage for exploring Crew's memory feature.

#### Understanding Memory in Crew

Memory in Crew refers to how contextual information is provided to large language models (LLMs) during each call. While you can manually manage memory by storing variables and passing them into tasks, Crew offers built-in constructs for memory management. This approach has pros and cons:

- **Pros** : Quick setup and use of well-designed memory handling.
- **Cons** : A learning curve and less visibility into prompt mechanics.

It's important to weigh these benefits and trade-offs when adopting Crew's memory framework.

#### Five Types of Memory in Crew

Crew provides five different types of memory frameworks:

- **Short Term Memory** : Stores recent interactions using a vector database in a retrieval-augmented generation (RAG) style. This allows agents to access relevant recent information during execution.
- **Long Term Memory** : Stores important information in a SQL database for longer-term recall, building knowledge over time.
- **Entity Memory** : Similar to short term memory but focused on entities such as people, places, and concepts, stored in a RAG database for vector similarity search.
- **Contextual Memory** : An umbrella term encompassing short term, long term, and entity memory, allowing combined querying and context passing to LLMs.
- **User Memory** : Stores user-specific information; currently, Crew supports this concept but requires manual querying and insertion into prompts.

For this project, we focus on contextual memory, which includes short term, long term, and entity memory.

#### Implementing Memory in the Stock Picker Project

We return to the stock picker project and edit the `crew.py` module. First, we import the necessary memory classes:

- `LongTermMemory`, `ShortTermMemory`, and `EntityMemory` from Crew memory.
- `RagStorage` for vector-based retrieval.
- `LongTermMemorySQLiteStorage` for SQL-based long term memory.

These imports prepare us to create memory objects for our agents.

#### Creating Memory Objects

We create three memory objects:

- **Short Term Memory** : Uses `RagStorage` with an OpenAI provider and an embedding model to generate vectors from text. The vector store is saved in a `memory` directory using Chroma.
- **Long Term Memory** : Uses `LongTermMemorySQLiteStorage` with a SQLite database file in the `memory` directory.
- **Entity Memory** : Also uses `RagStorage` with the same provider and embedding model, stored in the `memory` directory.

These objects enable different memory capabilities for the agents.

##### Integrating Memory into Crew

When creating the Crew instance, we enable memory by setting `memory=True` and passing the three memory objects:

- `short_term_memory`
- `long_term_memory`
- `entity_memory`

This simple configuration activates Crew's memory features for the project.

##### Enabling Memory for Specific Agents

We update the agent definitions to specify which agents use memory:

- The **Trading Company Finder** agent has `memory=True` to retain context.
- The **Financial Researcher** agent does not use memory, as it performs fresh research each time.
- The **Stock Picker** agent has `memory=True` to avoid recommending the same stock multiple times.

This selective enabling ensures appropriate use of memory per agent role.

##### Adjusting Prompts for Memory

It is important to ensure that the YAML prompt files clearly instruct agents to leverage memory. For example, prompts should specify not to recommend the same stock twice or to surface new companies. Since memory adds relevant context to prompts, clear instructions maximize its effectiveness.

#### Running the Stock Picker with Memory

After setting up memory, we run the stock picker project. Upon execution, a `memory` directory is created containing:

- A Chroma vector database for short term and entity memory.
- A SQLite database file for long term memory.

The system populates these data stores as agents interact, demonstrating memory in action. Although internal memory usage details are abstracted, the presence of these databases confirms successful memory integration.

#### Summary

This project showcased the ease of integrating multiple memory types in Crew:

- Short term memory with vector similarity queries.
- Long term memory with SQL queries.
- Entity memory for specific concepts.

By creating memory objects and enabling memory for agents, we enhanced the stock picker with contextual awareness. This concludes our tour of Crew's memory features and the stock picker project, which also demonstrated structured outputs, custom tools, and hierarchical processes.

#### Key Takeaways

- The Crew framework provides five types of memory: short term, long term, entity, contextual, and user memory.
- Short term memory uses vector databases for recent interactions, while long term memory uses SQL databases for persistent knowledge.
- Entity memory stores information about people, places, and concepts using vector similarity search.
- Enabling memory in Crew involves creating memory objects and setting `memory=true` for agents to utilize stored context.

### Crew AI for Coding Tasks: Agents That Generate & Run Python Code

#### Introduction to Coding Agents in Crew

We are going to work on creating an agent that knows how to write Python code and software, and more importantly, how to run it as well. This is a challenging and complex task, but it is possible to have an agent in the Crew environment with this capability. The agent can take a problem you set, write code to solve it, execute that code in a Docker container, and then interpret the results to take further action.

Running code in a Docker container provides a sandboxed, ring-fenced environment that prevents the code from damaging your computer. This advanced task is made simple in Crew by just enabling code execution with a single configuration flag. If Docker is installed, the code runs safely inside a container.

This kind of system is sometimes called a Coda agent or code agent. It not only generates Python code but also runs it as steps toward solving a larger problem. Our project for this week is to build such an agent that writes and runs code.

#### Setting Up the Crew Project

We begin by creating a new Crew project named `coda`. This scaffolds the necessary directories and files. We specify OpenAI as the provider and GPT as the model, without needing an API key for this setup.

#### Defining the Agent Configuration

In the configuration file, we define a single agent named `coda`. The agent's role is a Python developer tasked with writing Python code to achieve the given assignment. The process is:

- Plan how the code will work.
- Write the code.
- Run the code and check the output.

The backstory describes the agent as a seasoned Python developer skilled in writing clean, efficient code. We specify the model provider and name for clarity.

#### Defining the Task

We define a single task where the agent must write Python code to achieve the assignment. The output should be a text file containing both the code and its output. This ensures the agent not only writes code but also runs it and returns the results for verification.

#### Preparing the Crew Module

In the Crew module, we remove default templating and keep only the configuration relationships. We include a comment with a link to the Docker Desktop webpage for installing Docker, which is a one-click install for Mac, Windows, or Linux. Docker installation is necessary for running code safely in containers.

#### Creating the Coder Agent

We define the coder agent using the `@agent` decorator. The agent uses the configuration from the YAML file and has verbose output enabled. To enable code execution, we set `allow_code_execution` to true. We also specify `code_execution_mode` as `safe` to ensure code runs inside a Docker container, protecting the host system.

Additional parameters include:

- `max_execution_time` set to 30 seconds to limit how long code can run.
- `max_retry_limit` set to 5 to allow up to five attempts for code execution.

#### Finalizing the Task and Agent Setup

With the agent and task defined, we remove redundant expected output definitions since the task already specifies the expected output. The final step is to implement the Crew function method to tie everything together.

#### Key Takeaways

- Developed an agent capable of writing and executing Python code within a secure Docker environment.
- Demonstrated the simplicity of enabling code execution in Crew agents with minimal configuration.
- Emphasized the importance of sandboxing code execution to protect the host system.
- Illustrated the process of setting up a coding task and agent configuration in Crew.

### Create a Python-Writing AI Agent: Practical Implementation with Crew AI

#### Introduction

In this session, we focus on writing the crew function for our agent. However, it turns out that the default implementation already provides everything required. There is no need to write a custom crew function.

#### Setting Up the Main Function

The next step is to modify the main function. All unnecessary code is removed, and a new run function is written to execute the crew.

#### python Code Sample

```python
defrun():
    inputs = {"assignment": assignment}
    result = coder.crew.kickoff(inputs)
print(result)
```

#### Defining the Assignment

The assignment variable needs to be set. To ensure the agent genuinely executes code, a more challenging task is chosen instead of a simple 'Hello world' script. This prevents the agent from merely simulating output.

#### python Code Sample

```python
assignment = "Write a Python program to calculate the first 10,000 terms of the series: 1 minus a third plus a fifth minus a seventh plus ... Then multiply the total by four."
```

#### Understanding the Series

The series described is:

1−1/3+1/5−1/7+...

The agent is expected to sum the first 10,000 terms, multiply the result by four, and output the value. This is a classic, though slow, method to approximate **π**.

#### Running the Agent

The agent is run using the terminal. The command is executed, and the agent begins processing the assignment.

#### bash Code Sample

```bash
crew run
```

#### Reviewing the Output

The agent writes Python code to solve the assignment. It uses a technique involving (−1)**(**−**1**) to the power of the index to alternate signs, and divides by the appropriate odd number. The result is multiplied by four at the end, as required.

#### python Code Sample

```python
total = 0
terms = 10000
for i inrange(terms):
    total += ((-1) ** i) / (2 * i + 1)
result = total * 4
print(result)
```

#### Output and Verification

The output is approximately 3.14149**3.14149**, which is a rough approximation of π**π**. The agent also creates an output file containing the code and the result.

#### Reflection and Next Steps

The process demonstrates how straightforward it is to give coding skills to an agent. The underlying machinery, such as starting a Docker container, generating code, running it, and interpreting the result, works seamlessly. The next step is to extend this capability to build a full engineering crew capable of solving end-to-end problems.

#### Key Takeaways

- The default crew function is sufficient for running the agent; no custom implementation is needed.
- A challenging assignment was created to ensure the agent genuinely executes code rather than simulates output.
- The agent successfully wrote and executed Python code to approximate pi using a series, demonstrating its coding ability.
- The process highlights the ease of giving coding skills to an agent and sets the stage for building a full engineering crew.

## Day 5

### Building AI Teams: Configure Crew AI for Collaborative Development

#### Introduction to Building an AI Engineering Team

This marks the final day of our journey with Crew, the fifth day of week three. We are concluding our work with Crew on a high note by expanding on the project from day four. Today, we will transform our Coda into a fully functioning engineering team.

Our team will consist of an engineering lead, a backend engineer, a frontend engineer, and a test engineer. The engineering lead will oversee the work, depicted here as someone relaxed, embodying the leadership role. The backend engineer and frontend engineer will handle their respective development tasks, while the test engineer will rigorously test the outputs, attempting to break everything to ensure quality.

#### Setting Up the Crew Project

Let's begin by opening a terminal using Control + backtick. Navigate to the third directory and initialize a new Crew project named `engineering_team`.

We select the options as prompted: choose OpenAI as the provider, select GPT-4 or GPT-4 Mini as the model, and skip token creation. This generates the directory structure for our project.

Next, navigate into the `engineering_team/source/config` directory and open the `agents.yaml` file. Initially, it contains boilerplate agents such as the researcher and reporting analyst, which we will remove to define our custom agents.

#### Defining the Engineering Lead Agent

We start by defining the engineering lead agent. This agent directs the engineers by taking high-level requirements and preparing a detailed design for the backend developer.

Key attributes include:

- The design should be for a single Python module if there is only one developer.
- The design must describe the functions and method signatures within the module.
- The Python module should be self-contained and ready for testing or for building a simple UI.
- Input attributes include the requirements, module name, and class name.
- The backstory describes the agent as a seasoned engineering lead skilled in writing clear and concise designs.

We configure this agent to use the GPT-4 model for comprehensive and extensive solutions.

#### Defining the Backend Engineer Agent

The backend engineer is a Python developer responsible for implementing the design provided by the engineering lead.

Attributes include:

- Receives the design, requirements, module name, and class name.
- Backstory: a Python engineer with a knack for writing clean, efficient code who follows design instructions carefully.
- Uses the Claude 3.7 Sonnet latest model to generate code.

This agent writes the Python module that realizes the design specifications.

#### Defining the Frontend Engineer Agent

The frontend engineer specializes in creating a Gradio UI to demonstrate the backend module.

Details include:

- Writes a simple Gradio UI in a single file named `App.py` located in the same directory as the backend module.
- Receives the requirements and the backend class to demonstrate.
- Backstory: a seasoned engineer highly skilled at writing simple Gradio UIs.
- Uses the Claude model for UI generation.

The UI is intended to be a prototype or demo, kept simple and clean for ease of use.

#### Defining the Test Engineer Agent

The test engineer is a Python developer focused on writing unit tests for the backend module.

Attributes:

- Creates a test file named `test_<module_name>.py` in the same directory as the backend module.
- Backstory: a seasoned QA engineer and software developer skilled in writing great unit tests for Python code.
- Uses the DeepSeek Chat model for code generation.

This agent ensures the backend code is thoroughly tested, though it does not test the UI.

#### Configuring Tasks for Each Agent

Each agent is assigned a specific task, creating a one-to-one mapping between tasks and agents.

- **Design Task:** Assigned to the engineering lead. The task is to take high-level requirements and prepare a detailed design for the engineer. The output must be in markdown format only, avoiding code generation at this stage. The output file is named using the template `module_name_design`.
- **Code Task:** Assigned to the backend engineer. The task is to write a Python module implementing the design to meet the requirements. The output must be raw Python code without markdown formatting or code block delimiters to ensure valid Python files. This task uses the design task as context.
- **Frontend Task:** Assigned to the frontend engineer. The task is to write a Gradio UI in `App.py` demonstrating the backend class. The UI should be simple and clean. The output is raw Python code only. This task uses the code task output as context.
- **Test Task:** Assigned to the test engineer. The task is to write unit tests for the backend module, outputting raw Python code without markdown formatting. This task depends on the code task output.

#### Important Notes on Output Formatting

It is crucial to instruct agents to output only raw Python code without any markdown formatting, code block delimiters, or backticks. This prevents invalid Python files caused by extraneous formatting such as triple backticks or language tags.

This explicit instruction ensures that the generated code is immediately usable and integrates smoothly into the project.

#### Key Takeaways

- Configured a collaborative AI engineering team using Crew with distinct roles: engineering lead, backend engineer, frontend engineer, and test engineer.
- Defined clear agent roles and responsibilities with detailed backstories and instructions for design, coding, UI development, and testing.
- Utilized multiple language models (OpenAI GPT-4, Claude, DeepSeek) to diversify capabilities across agents.
- Structured tasks with explicit output formatting requirements to ensure clean code generation and seamless integration between agents.

### Collaborative AI Agent Development for a Stock Trading Framework

#### Introduction to the Crew Module

It is time to proceed to the crew module. This is the next step. The intention is to remove all unnecessary components, keeping only the essential connections to the YAML files. Everything else will be removed, and the focus will be on defining the agents.

#### Defining Agents

The first agent is called the engineering lead. Suggestions from the code assistant are helpful, but not perfect, as the engineering lead does not need the ability to execute code. Its purpose is solely to design components.

For the backend engineer, code execution is required. The code execution must be safe, running inside a Docker container. The maximum execution time should be set to a few minutes, not excessively long. The maximum number of retries is set to five.

The frontend engineer is responsible for writing frontend code, but will not execute it, as this would launch a Gradio UI in the Docker container, which is not desired. The frontend engineer will focus on creation tasks only.

The test engineer must both write and run unit tests. It is allocated a couple of minutes for execution and five retries as well.

##### python Code Sample

```python
engineering_lead = Agent(
    name="Engineering Lead",
    can_execute_code=False
)

backend_engineer = Agent(
    name="Backend Engineer",
    can_execute_code=True,
    execution_env="docker",
    max_execution_time=180,
    max_retries=5
)

frontend_engineer = Agent(
    name="Frontend Engineer",
    can_execute_code=False
)

test_engineer = Agent(
    name="Test Engineer",
    can_execute_code=True,
    execution_env="docker",
    max_execution_time=120,
    max_retries=5
)
```

#### Defining Tasks

Next, the tasks for each agent are defined. The design task is straightforward. The code assistant is expected to assist with the remaining tasks, including the code, frontend, and test tasks. The tasks are now complete, with nothing missing.

##### python Code Sample

```python
design_task = Task(
    agent=engineering_lead,
    description="Design the system architecture."
)

code_task = Task(
    agent=backend_engineer,
    description="Implement backend logic."
)

frontend_task = Task(
    agent=frontend_engineer,
    description="Develop frontend interface."
)

test_task = Task(
    agent=test_engineer,
    description="Write and run unit tests."
)
```

#### Defining the Crew

Now, it is time to define the crew. It is important to be mindful when using code assistants, as language models often generate excessive code. Many users encounter issues due to over-generation. In this case, it is unnecessary to list all agents explicitly; instead, reference `self.agents` and `self.tasks`. The process should be set to sequential, and verbosity enabled. The function is typically named `crew`.

##### python Code Sample

```python
defcrew(self):
return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process="sequential",
        verbose=True
    )
```

#### Implementing the Run Function

The next step is to implement the run function. All unnecessary code is removed, leaving a simple structure. Variables for requirements, module name, and class name are defined. The engineering team is initiated by calling the decorated crew method with the appropriate inputs.

##### python Code Sample

```python
requirements = ...  # Define requirements
module_name = ...   # Define module name
class_name = ...    # Define class name

engineering_team = self.crew(requirements, module_name, class_name)
```

#### The Coding Challenge: Account Management System

A coding challenge is presented to the team of agents. The requirements are as follows:

- Build a simple account management system for a trading simulation platform.
- The system must allow users to create accounts, deposit funds, and withdraw funds.
- Users can record buying or selling shares, specifying quantity.
- The system calculates the total value of the user's portfolio and profit or loss from the initial deposit.
- It reports holdings and PNL at any time, and lists all user transactions.
- The system prevents users from withdrawing funds resulting in a negative balance, buying shares they cannot afford, or selling shares they do not possess.
- The system has access to a function `get_share_price`, which returns the current price of a share, including a fixed price implementation for three shares.

This framework simulates trading activity and is a substantial task to implement correctly.

##### python Code Sample

```python
defget_share_price(symbol):
    prices = {
"AAPL": 150,
"GOOG": 2800,
"TSLA": 700
    }
return prices.get(symbol, 0)
```

#### Motivation for the Challenge

The reason for this challenge is to prepare for the final week of the course, where agent traders will be built using OpenAI's agents SDK and MCP. The goal is to create agents capable of monitoring financial markets, analyzing real-time prices, and making trading decisions. A lightweight account management framework is required for these experiments, as existing frameworks are too complex. By building this system now, it will serve as a reusable foundation for future projects, saving time and effort.

#### Conclusion

With the introduction complete, it is time to attempt running the system.

#### Key Takeaways

- Defined specialized agents for engineering, backend, frontend, and testing roles in a collaborative AI development framework.
- Outlined tasks for each agent, ensuring clear separation of responsibilities.
- Emphasized the importance of minimal, maintainable code when using language models for code generation.
- Introduced a coding challenge to build a lightweight account management system for a trading simulation platform, forming the basis for future agent-based trading experiments.

### Building a Trading Application Using GPT-4o & Claude

#### Debugging and Setup Challenges

Initially, I noticed that the module name and class name were missing in the setup. The module name should be `accounts.py` and the class name should be `Account`. Additionally, there were formatting issues in the task's YAML file, including stray tabs that caused improper formatting. When I tried to run the code, it failed with an obscure error message and a long stack trace, making it difficult to identify the problem immediately.

For newcomers to the framework, this lack of clear error messages can be a painful experience. However, this is part of the trade-off when using such a framework: you get a lot out of the box, including memory management and code execution features, but some internals are hidden. This can make debugging more challenging when things go wrong.

#### Running the Engineering Team's Code

After fixing the issues, I navigated to the engineering team directory and ran the command `crew run`. The process started with the engineering lead, which is GPT-4o in my setup. You may have chosen a different model, such as LLaMA. However, running this with LLaMA can be very challenging and may have limited success depending on the model variant.

I saved the results in the `example_output` folder so you can review them even if you cannot run the code yourself. Using GPT-4o or GPT-4 Mini should work fine.

The design phase completed successfully, and the task was passed to the Python engineer. The entire process took about five minutes, which is expected, especially with Deep Seek enabled, which can slow things down.

#### Reviewing the Generated Code

Looking into the output folder, I found many files. Starting with the design document, it was in markdown format and contained method signatures and design details.

The main code file, `accounts.py`, included a dummy `get_share_price` function returning prices for Apple, Tesla, and Google to seed the system. The `Account` class was well-defined with methods for depositing, withdrawing, and managing accounts, all accompanied by docstrings.

The implementation looked comprehensive, including methods to calculate profit or loss, get holdings (returning a copy to avoid side effects), and other necessary functionalities. The code quality was impressive and aligned with best practices.

The test file `test_accounts.py` contained appropriate assertions and unit test scaffolding, ensuring the code was well-tested.

There was also an `app.py` file, which I planned to explore separately.

#### Running the Application and Installing Dependencies

I opened a terminal and navigated to the output folder to run the application. Initially, running `app.py` failed due to a missing module: Gradio.

I installed Gradio using the command `uv add gradio`. After installation, running `app.py` again started the application successfully. It loaded the necessary Gradio dependencies and launched the app.

#### Exploring the User Interface

The application presented a user interface with tabs labeled "Account Management," "Trading," and "Reports." The interface was well-organized and visually appealing.

I created an account by providing a user ID and an initial deposit of 10,000. The account was created successfully, and the holdings initially showed no shares.

In the trading tab, I bought one share of Apple. The purchase was successful, and the cash balance decreased accordingly. The portfolio value reflected the total value of holdings, and the holdings tab showed one share of Apple at the current price.

The reports tab displayed portfolio value, profit or loss, current holdings, and transaction history, including deposits and share purchases.

#### Testing Error Handling and Selling Shares

I attempted to sell one share of Tesla, which I did not own. The application correctly returned an error message: "Insufficient shares to sell."

Then, I sold one share of Apple successfully, which updated the holdings to zero.

The transaction history reflected both the purchase and sale of Apple shares accurately.

#### Final Thoughts

I was astonished by the quality of the user interface and the overall application. This was a raw, unedited reaction, and the interface was much sharper and better organized than previous attempts with GPT-4 or GPT-4 Mini.

The collaboration between GPT-4o, Claude 37, and Deep Seek produced a sophisticated trading platform with an impressive user interface.

I plan to provide example outputs for both GPT-4 Mini and this version so you can compare the differences and learn from the results.

#### Key Takeaways

- The framework provides a powerful head start but can be challenging to debug due to hidden internals.
- The generated code included comprehensive class methods with proper docstrings and thoughtful implementations.
- The trading application user interface built with Gradio was well-organized, functional, and exceeded expectations.
- Collaboration between GPT-4o, Claude, and Deep Seek enabled the creation of a sophisticated trading platform.

### From Single Modules to Complete Systems: Advanced CrewAI Techniques

I am genuinely impressed by how well that project performed. It was surprisingly easy to assemble a crew of different agents to build the product. The user interface worked immediately, appearing and running smoothly with great functionality. The system included both front-end and back-end components that integrated seamlessly.

I hope you are experiencing similar results and perhaps some disbelief at the ease and effectiveness. I have saved that particular example in a file named `example Output new`. Additionally, there are a couple of other examples available for you to try out. However, you should also experiment yourself by trying different models and configurations.

This week includes important projects designed to deepen your learning. The best way to learn is by building things yourself, taking examples like this and constructing them step by step. Approach it piece by piece, gradually adding complexity.

One straightforward way to enhance your project is to grow your team. For instance, the role I called "test engineer" was not a traditional test engineer but someone who wrote test cases. You could have a dedicated test engineer responsible for writing and executing a test plan. You might also add a business analyst to flesh out requirements or develop a richer user interface. The possibilities are vast; we are only scratching the surface with our four-person team. You can continue expanding and experimenting with different models to see where it leads.

However, the more challenging task this week is to move beyond producing just one Python module for the back-end code, along with the front-end and test modules. Currently, the system is quite linear with a fixed single module at the start. It would be much better if your team could build an entire system piece by piece, working on different classes to create various modules and then assembling them together.

This introduces a problem: you need a workflow that is more interactive. Potentially, different classes would be created by different agents. There are several ways to achieve this. One is to use structured outputs to gain clarity from the engineering lead about who is responsible for what. Structured outputs can help construct the different modules that need to be written.

Ultimately, you will want to call an engineer a dynamic number of times, depending on how many modules the engineering lead wants to create. It is not fixed at the time of writing the code how many tasks will run. Crew supports this and makes it quite easy. You can create a task object at runtime while the system is running.

A task object can include a callback field. The callback, associated with the agent, can create another task. This approach allows you to build a more dynamic system where completing one task triggers another. You can assign tasks for each module that needs to be built. This is the challenge for you: add structured outputs and dynamic task creation so that an entire set of modules can be created, enabling you to build a complete system.

You do not necessarily need to build a specific system provided here. Instead, apply this concept to your own work. Think of a system you would like to build, whether it is a website, an e-commerce platform, or something to organize medical records. Whatever your profession or line of business, consider the challenge you could set for your crew to build a dynamic system involving multiple modules.

While working on this, be sure to share your progress. Posting updates on LinkedIn can generate excitement. Tag me so I can engage and help increase visibility. These projects are valuable for building and demonstrating your expertise to others.

To clarify, if you want to work with callbacks, you do so at the task level, not the agent level. According to the Crew documentation, when creating a task, you specify a callback by setting `callback=` to the name of a function that should be called when the task completes. This function can then create new tasks dynamically.

The documentation also explains that you can create tasks from YAML configurations or by passing the full code version directly. Instead of specifying YAML, you can pass the description and expected output in code. There is a lot of interesting information worth exploring, including task guardrails, which are similar to concepts in the OpenAI Agents SDK.

Guardrails provide a way to validate and transform outputs before they are passed to the next task. Unlike OpenAI's constraints, guardrails in Crew can be implemented at any task, not just the first or last. There is also information on handling errors with guardrails and on structured outputs, such as using output pedantic or output JSON formats.

Integrating tools with tasks is another feature. You can create a task with tools, such as the surfer dev tool we used earlier. Tasks can refer to other tasks, and outputs are automatically related to subsequent tasks. You can define the context to be used for this integration.

There is also support for asynchronous execution of tasks. Although we have not used async this week, it will return in future lessons. You can read about asynchronous execution of Crew tasks in the documentation.

The callback mechanism allows you to implement a callback function that is called when a task completes. This can trigger the creation of new tasks dynamically, enabling complex workflows.

I encourage you to read more about guardrails and callbacks in the documentation. These features will be helpful when building advanced flows where completing one task triggers multiple others dynamically.

Sadly, this marks the end of Crew week and week three overall. We accomplished great things, including building fun projects like the stock picker and the engineering team system. I hope you enjoyed it and share my enthusiasm for Crew. While I prefer OpenAI Agents SDK, I also appreciate Crew and look forward to moving to a more heavyweight framework, LangChain, in week four. It will be an exciting continuation.

#### Key Takeaways

- Successfully built a multi-agent system with a working front end and back end.
- Encouraged experimentation with different models and team roles to enhance system complexity.
- Introduced dynamic task creation and structured outputs for building modular systems.
- Highlighted the importance of callbacks, guardrails, and asynchronous execution in advanced workflows.

# Project

## Free AI Model Searcher

## Study Buddy Crew

**Scenario** : Helping students/learners efficiently master knowledge

**Agents**

- **Curriculum Planner** : Generates a study plan based on the learner’s goals
- **Explainer** : Breaks down complex concepts into simple, easy-to-understand explanations
- **Quiz Master** : Automatically creates quizzes (multiple-choice and fill-in-the-blank)
- **Review Coach** : Summarizes learning progress and provides improvement suggestions

  **Highlight** : By leveraging the memory feature, the system can continuously track the learner’s progress and build a personalized learning profile.
