# chat bubble
```python
from IPython.display import HTML
HTML("""<style>
.chat-bubble { padding: 12px 16px; border-radius: 18px; margin: 4px 0; max-width: 70%; display: inline-block;}
.chat-bubble-primary { background-color: #007bff; color: white; }
.chat-bubble-secondary { background-color: #f1f3f4; color: black; }
.chat { display: flex; margin: 8px 0; }
.chat-start { justify-content: flex-start; }
.chat-end { justify-content: flex-end; }
</style>""")



def chat_bubble(m):
    is_user = m["role"] == "user"
    if m["role"] == "system":
        return Details(
            Summary("System Prompt"),
            Div(render_md(m["content"]), cls="chat-bubble chat-bubble-secondary"),
            cls="chat chat-start"
        )
    return Div(
        Div(render_md(m["content"]), cls=f"chat-bubble {'chat-bubble-primary' if is_user else 'chat-bubble-secondary'}"),
        cls=f"chat {'chat-end' if is_user else 'chat-start'}"
    )

from msglm import mk_msg_anthropic as mk_msg, mk_msgs_anthropic as mk_msgs

msgs = [
    {"role": "system", "content": "You are a helpful assistant"},
    *mk_msgs(["user message", "assistant response"])
]

Container(*L(msgs).map(chat_bubble))
```
