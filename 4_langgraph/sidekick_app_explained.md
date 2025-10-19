# Sidekick LangGraph App Explained

This guide walks through the Sidekick personal co-worker application from the `4_langgraph` module. We'll unpack every component so you can rebuild or customize the app without hunting for extra references.

---

## 1. High-Level Flow

1. A Gradio interface (`app.py`) hosts the chat UI and keeps a shared `Sidekick` instance in memory.
2. The `Sidekick` class (`sidekick.py`) prepares:
   - Tool integrations (Playwright, file tools, search, Python REPL, Wikipedia, push notifications).
   - Two coordinated language models: a **worker** that performs tasks with tools and an **evaluator** that scores each worker response.
   - A LangGraph **state machine** describing how the worker and evaluator interact.
3. Incoming user messages run through the LangGraph pipeline until the evaluator declares success or more user input is required.
4. Results stream back into the Gradio chatbot along with evaluator feedback. Cleanup hooks close Playwright resources when the UI resets.

---

## 2. Gradio Front-End (`app.py`)

### 2.1 Bootstrapping the Sidekick

```python
async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick
```

- Creates a `Sidekick` instance and awaits its asynchronous `setup` (which in turn loads tools and compiles the LangGraph pipeline).
- Returns the instance so Gradio can stash it inside a `gr.State` component.

### 2.2 Handling Conversations

```python
async def process_message(sidekick, message, success_criteria, history):
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick
```

- Gradio passes the current `Sidekick`, latest user message, success criteria text, and the chat history.
- `run_superstep` executes the LangGraph over the latest message and returns an updated transcript. Gradio re-saves the `sidekick` state for future turns.

### 2.3 Reset and Cleanup

```python
async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick
```

- Completely replaces the Sidekick and clears all UI widgets.
- Passing `free_resources` to `gr.State(delete_callback=...)` guarantees Playwright and the browser close if the UI session ends.

### 2.4 UI Layout

- `gr.Chatbot` renders the conversation.
- Two `gr.Textbox` widgets capture the prompt and optional success criteria.
- A “Go!” button and form submissions trigger `process_message`; a “Reset” button calls `reset`.
- `ui.load(setup, [], [sidekick])` ensures setup runs as soon as the interface mounts.

> **Takeaway:** `app.py` is a thin orchestration layer—its main job is to create and share the `Sidekick` instance and surface LangGraph results in a pleasant UI.

---

## 3. Tooling Layer (`sidekick_tools.py`)

### 3.1 Loading Environment Configuration

```python
load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
```

- Environment variables supply credentials for optional integrations (push notifications, Google Serper, etc.).

### 3.2 Browser Automation Tools

```python
async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright
```

- Starts Playwright and Chrome, then wraps them inside LangChain’s `PlayWrightBrowserToolkit`.
- Returns both the tool objects (used by Sidekick) and the raw browser/playwright handles (needed for cleanup).

### 3.3 Miscellaneous Productivity Tools

```python
async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, ...)
    file_tools = get_file_tools()
    tool_search = Tool(name="search", func=serper.run, ...)
    wiki_tool = WikipediaQueryRun(...)
    python_repl = PythonREPLTool()
    return file_tools + [push_tool, tool_search, python_repl, wiki_tool]
```

- Wraps custom helpers and LangChain community tools into a single list.
- `FileManagementToolkit` gives the agent read/write access to the local `sandbox` directory.
- `PythonREPLTool` lets the agent run Python snippets (output only appears if the agent uses `print`).

> **Takeaway:** `sidekick_tools.py` delivers a rich toolset that the LangGraph worker can invoke when solving user requests.

---

## 4. State Management (`sidekick.py`)

### 4.1 Shared Data Model

```python
class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool
```

- LangGraph requires an explicit schema. `add_messages` merges new chat content into the history automatically.
- Tracks evaluator feedback and overall progress flags.

### 4.2 Evaluator Output Schema

```python
class EvaluatorOutput(BaseModel):
    feedback: str
    success_criteria_met: bool
    user_input_needed: bool
```

- The evaluator LLM emits structured feedback by binding the model to a Pydantic schema with `with_structured_output`.

### 4.3 Sidekick Lifecycle

```python
class Sidekick:
    def __init__(self):
        self.tools = None
        self.graph = None
        self.sidekick_id = str(uuid.uuid4())
        self.memory = MemorySaver()
```

- `sidekick_id` uniquely identifies each Gradio session.
- `MemorySaver` persists intermediate graph states keyed by `thread_id` so multi-turn conversations resume smoothly.

### 4.4 `setup`: Wiring Tools and Models

```python
async def setup(self):
    self.tools, self.browser, self.playwright = await playwright_tools()
    self.tools += await other_tools()
    worker_llm = ChatOpenAI(model="gpt-4o-mini")
    self.worker_llm_with_tools = worker_llm.bind_tools(self.tools)
    evaluator_llm = ChatOpenAI(model="gpt-4o-mini")
    self.evaluator_llm_with_output = evaluator_llm.with_structured_output(EvaluatorOutput)
    await self.build_graph()
```

1. Loads the async Playwright tool suite and adds other tools.
2. Creates a worker LLM and binds every tool so the model can produce `tool_calls` in responses.
3. Spawns an evaluator LLM configured to emit validated `EvaluatorOutput` objects.
4. Compiles the LangGraph state machine via `build_graph`.

---

## 5. LangGraph Workflow

### 5.1 Worker Node

```python
def worker(self, state: State) -> Dict[str, Any]:
    system_message = f"""You are a helpful assistant..."""
    if state.get("feedback_on_work"):
        system_message += "Previously you thought..."
    messages = state["messages"]
    ... # inject SystemMessage if missing
    response = self.worker_llm_with_tools.invoke(messages)
    return {"messages": [response]}
```

- Builds a dynamic system prompt that includes current success criteria and any evaluator feedback.
- Ensures the conversation begins with a `SystemMessage` so the worker always sees the latest instructions.
- Invokes the tool-enabled LLM; the return value may include tool calls.

### 5.2 Tool Router

```python
def worker_router(self, state: State) -> str:
    last_message = state["messages"][-1]
    return "tools" if last_message.tool_calls else "evaluator"
```

- If the worker requested a tool, LangGraph should route next to `ToolNode` (which executes the tool and appends the result). Otherwise the evaluator reviews the answer.

### 5.3 Evaluator Node

```python
def evaluator(self, state: State) -> State:
    last_response = state["messages"][-1].content
    ...
    eval_result = self.evaluator_llm_with_output.invoke(evaluator_messages)
    new_state = {
        "messages": [{"role": "assistant", "content": f"Evaluator Feedback on this answer: {eval_result.feedback}"}],
        "feedback_on_work": eval_result.feedback,
        "success_criteria_met": eval_result.success_criteria_met,
        "user_input_needed": eval_result.user_input_needed,
    }
    return new_state
```

- Supplies the evaluator with the entire formatted conversation, the success criteria, and the worker’s latest answer.
- The evaluator responds with detailed feedback and success flags, which the graph stores back into the global state.
- Instead of using LangChain messages for feedback, a simple dict goes into the message list—LangGraph merges it seamlessly thanks to `add_messages`.

### 5.4 Routing After Evaluation

```python
def route_based_on_evaluation(self, state: State) -> str:
    if state["success_criteria_met"] or state["user_input_needed"]:
        return "END"
    else:
        return "worker"
```

- Success or a request for user input exits the graph. Otherwise, the worker gets another shot armed with evaluator feedback.

### 5.5 Building the Graph

```python
async def build_graph(self):
    graph_builder = StateGraph(State)
    graph_builder.add_node("worker", self.worker)
    graph_builder.add_node("tools", ToolNode(tools=self.tools))
    graph_builder.add_node("evaluator", self.evaluator)
    graph_builder.add_conditional_edges("worker", self.worker_router, {"tools": "tools", "evaluator": "evaluator"})
    graph_builder.add_edge("tools", "worker")
    graph_builder.add_conditional_edges("evaluator", self.route_based_on_evaluation, {"worker": "worker", "END": END})
    graph_builder.add_edge(START, "worker")
    self.graph = graph_builder.compile(checkpointer=self.memory)
```

- The LangGraph pipeline:
  1. **START → worker**
  2. **worker → tools** (if tool call) → **worker** (LLM sees tool result)
  3. **worker → evaluator** (if no tool call)
  4. **evaluator → worker** (continue) or **evaluator → END** (break loop)
- `compile(checkpointer=self.memory)` makes the graph resumable across messages using `thread_id`.

### 5.6 Running a Superstep

```python
async def run_superstep(self, message, success_criteria, history):
    config = {"configurable": {"thread_id": self.sidekick_id}}
    state = {
        "messages": message,
        "success_criteria": success_criteria or "The answer should be clear and accurate",
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False,
    }
    result = await self.graph.ainvoke(state, config=config)
    user = {"role": "user", "content": message}
    reply = {"role": "assistant", "content": result["messages"][-2].content}
    feedback = {"role": "assistant", "content": result["messages"][-1].content}
    return history + [user, reply, feedback]
```

- Passes the fresh message as the `messages` field while leaving other state slots blank.
- Calls `ainvoke` to run the whole graph asynchronously. LangGraph internally stores checkpoints so follow-up turns continue from the same state machine run.
- Extracts the assistant’s reply (penultimate message) and evaluator feedback (last message) for the chat transcript.

### 5.7 Resource Cleanup

```python
def cleanup(self):
    if self.browser:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.browser.close())
            if self.playwright:
                loop.create_task(self.playwright.stop())
        except RuntimeError:
            asyncio.run(self.browser.close())
            if self.playwright:
                asyncio.run(self.playwright.stop())
```

- Ensures Playwright doesn’t leave orphaned browser processes, whether the caller is inside an event loop or not.

---

## 6. Putting It All Together

The conversation loop looks like this:

1. **User submits prompt** via Gradio → `process_message`.
2. **LangGraph Worker** crafts a response; if a tool is required, a `tool_call` triggers the `ToolNode` to run it and feed the output back to the worker.
3. **Evaluator** inspects the worker’s message:
   - If success criteria satisfied → graph ends.
   - If improvements needed → feedback inserted and control returns to the worker for another attempt.
   - If the worker clearly needs user input → conversation ends with a clarification request.
4. **Gradio UI** displays both the assistant’s answer and evaluator feedback so the user can see the reasoning and adjust requirements.
5. **Reset/Cleanup**: If the session resets, `free_resources` destroys the Playwright session and stops background processes.

---

## 7. Building Your Own Sidekick

To adapt or rebuild this app:

1. **Define your state schema** with everything the graph needs to track (messages, success flags, external context, etc.).
2. **Collect tools** in one place. Return both the tool objects and any handles you’ll need for teardown.
3. **Bind models**:
   - `ChatOpenAI().bind_tools(tools)` for the acting agent.
   - `ChatOpenAI().with_structured_output(YourSchema)` for critics/evaluators.
4. **Write worker/evaluator functions** that accept and return portions of the state dictionary.
5. **Assemble the graph** with `StateGraph`, add nodes, add conditional edges, and compile with a checkpointer if you need multi-turn persistence.
6. **Integrate with a UI or API**:
   - For Gradio, keep the agent in `gr.State` and wire async callbacks to `ainvoke`.
   - For FastAPI or other backends, you can store the agent in dependency injection or session storage.
7. **Handle cleanup** for any external resources.

> **Pro tip:** Treat LangGraph like a visual workflow engine. Each function node is independent and deterministic—maintain pure inputs/outputs, and let the graph manage sequencing and branching.

---

## 8. Knowledge Integration with LangGraph

- **Tool Augmentation:** Binding tools directly to the worker LLM allows it to decide dynamically when and how to fetch external information (web search, Wikipedia, browsing, file I/O, Python execution).
- **Evaluator Feedback Loop:** The evaluator’s structured feedback acts as knowledge distillation. By feeding `feedback_on_work` back into the worker’s system prompt, the agent keeps refining answers until they pass the rubric.
- **Checkpointed State:** `MemorySaver` keeps threading information so LangGraph can resume the conversation across supersteps, effectively maintaining long-term memory.
- **Success Criteria Alignment:** The user-controlled success criteria text flows through the entire pipeline, letting the evaluator enforce goal-specific quality gates.

---

## 9. Next Steps

- Swap in different tools (e.g., company APIs, knowledge bases) by extending `other_tools`.
- Add more LangGraph nodes (researcher, summarizer, planner) and route among them before reaching the evaluator.
- Persist evaluator feedback for analytics or automated quality control dashboards.
- Wrap the LangGraph invocation in tracing (LangSmith, OpenTelemetry) for observability.

With this breakdown, you should be ready to extend Sidekick or construct a similar LangGraph-driven co-worker tailored to your own workflows.
