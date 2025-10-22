"""A multi-modal chat interface using Autogen and Gradio.
  This example demonstrates how to build a chat interface that can handle both text and image inputs,
  and produce structured outputs using Pydantic models.
  """

import gradio as gr
import dotenv
from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core import Image as AGImage
from pydantic import BaseModel, Field
from typing import Literal

dotenv.load_dotenv(override=True)


class ImageDescription(BaseModel):
    scene: str = Field(description="Briefly, the overall scene of the image")
    message: str = Field(
        description="The point that the image is trying to convey")
    style: str = Field(description="The artistic style of the image")
    orientation: Literal["portrait", "landscape", "square"] = Field(
        description="The orientation of the image")


def create_image_description(content: ImageDescription) -> str:
    return f"""### Image Description

**Scene:** {content.scene}

**Message:** {content.message}

**Style:** {content.style}

**Orientation:** {content.orientation}"""


model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
agent = AssistantAgent(
    name="multimodal_agent",
    model_client=model_client,
    system_message="You are a helpful assistant that can process text and images.",
    model_client_stream=True,
    output_content_type=ImageDescription,
)


async def chat(message, history, image):
    # Handle the case when image is None
    if image is None:
        user_message = TextMessage(content=message, source="user")
    else:
        # Convert PIL Image to AGImage
        img = AGImage(image)
        user_message = MultiModalMessage(
            content=[message, img], source="user")

    response = await agent.on_messages(
        [user_message],
        cancellation_token=CancellationToken()
    )

    if isinstance(response.chat_message.content, ImageDescription):
        assistant_content = create_image_description(
            response.chat_message.content)
    else:
        assistant_content = response.chat_message.content

    updated_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": assistant_content}
    ]
    return updated_history

with gr.Blocks() as demo:
    gr.Markdown("## Autogen")
    gr.Markdown("""
    - Implement Multi-modal conversation
    - Structured outputs
    - Langchain tools
    - Team interaction with evaluation agents
                """)

    # # Example: Image Upload and Display
    # gr.Markdown("### Example: Upload and Display Image")
    # with gr.Row():
    #     with gr.Column():
    #         image_input = gr.Image(label="Upload Image", type="pil")
    #         upload_btn = gr.Button("Display Image", variant="primary")
    #     with gr.Column():
    #         image_output = gr.Image(label="Displayed Image")

    # upload_btn.click(
    #     fn=lambda img: img,
    #     inputs=image_input,
    #     outputs=image_output
    # )

    # gr.Markdown("---")
    # gr.Markdown("### Chat Interface")
    with gr.Row():
        image_input = gr.Image(label="Upload Image", type="pil")
        chatbox = gr.Chatbot(label="Chat Interface", type="messages")

    message = gr.Textbox(
        show_label=False, placeholder="Type your message here..."
    )

    message_submit = message.submit(
        chat, [message, chatbox, image_input], chatbox)
    message_submit.then(lambda: gr.update(value=""), None,
                        message, show_progress=False)
    clear_btn = gr.Button("Clear", variant="stop")
    clear_btn.click(lambda: ([], ""), None, [chatbox, message], queue=False)

demo.launch(
    server_name="0.0.0.0",
    server_port=8000,
    inbrowser=True
)
