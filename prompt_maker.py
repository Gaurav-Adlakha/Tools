from fasthtml.common import *
from monsterui.all import *
import os
import asyncio
from dotenv import load_dotenv
import litellm
import json

load_dotenv()

# App setup with MonsterUI blue theme
app,rt = fast_app(
    hdrs=Theme.blue.headers(),
    live=True,   # Enable live reload
    debug=True   # Enable debug mode for better error messages
)

components = [("role", "Role & Persona"), ("task", "Task Definition"), ("format", "Output Format"), ("examples", "Examples")]
models = [("gpt-4", "GPT-4"), ("gpt-3.5-turbo", "GPT-3.5"), ("claude-3", "Claude 3")]

@rt
def index():
    return Titled("Simple Prompt Maker", 
        Container(
            H1("AI Prompt Maker"),
            Form(
                Grid(
                    Card(
                        H3("Select & Customize Components"),
                        *[Div(LabelCheckboxX(comp[1], name="components", value=comp[0], cls='mb-2'), TextArea(placeholder=f"Enter your {comp[1].lower()}...", name=f"{comp[0]}_text", rows=2, cls='w-full mt-1 mb-3')) for comp in components]
                    ),
                    Card(
                        H3("Configuration"),
                        Select(*[Option(model[1], value=model[0]) for model in models], name="model", cls='w-full mb-4'),
                        H4("Main Criteria"),
                        TextArea(placeholder="Describe what you want your prompt to do...", name="criteria", rows=6, cls='w-full mb-4'),
                        Button("Generate Prompt", cls=ButtonT.primary, hx_post="/generate", hx_include="form", hx_target="#output")
                    ),
                    cols=2, gap=4
                ),
                Card(
                    H3("Generated Prompt"),
                    Div("Your prompt will appear here...", id="output", cls='border p-4 min-h-32')
                )
            )
        )
    )

@rt("/copy")
def copy_prompt(): return Script("navigator.clipboard.writeText(document.getElementById('prompt-text').textContent); alert('Copied!');")


@rt("/generate", methods=["POST"])
async def generate(request):

    form_data = await request.form()
    criteria = form_data.get("criteria", "")
    components = form_data.getlist("components")
    model = form_data.get("model", "gpt-3.5-turbo")
    role_text = form_data.get("role_text", "")
    task_text = form_data.get("task_text", "")
    format_text = form_data.get("format_text", "")
    examples_text = form_data.get("examples_text", "")
    
    if not criteria.strip(): return Div("Please enter some criteria first!", cls='text-red-500')
    
    prompt_parts = []
    if "role" in components: prompt_parts.append(f"# Role & Persona\n{role_text if role_text.strip() else 'You are an expert assistant with deep knowledge in the relevant field.'}")
    if "task" in components: prompt_parts.append(f"# Task\n{task_text if task_text.strip() else criteria}")
    if "format" in components: prompt_parts.append(f"# Output Format\n{format_text if format_text.strip() else 'Provide a clear, well-structured response that is easy to understand.'}")
    if "examples" in components: prompt_parts.append(f"# Examples\n{examples_text if examples_text.strip() else 'Include relevant examples to illustrate key points where appropriate.'}")
    
    if not prompt_parts: prompt_parts.append(f"# Request\n{criteria}")
    
    final_prompt = "\n\n".join(prompt_parts)
    
    return Div(
        DivFullySpaced(P(f"Model: {model}", cls='font-bold'), Button("Copy", hx_get="/copy", cls=ButtonT.ghost)),
        Pre(final_prompt, id="prompt-text", cls='border p-4 rounded bg-gray-50 text-sm whitespace-pre-wrap mt-2')
    )
    
serve()

