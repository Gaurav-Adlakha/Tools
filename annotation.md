## FastHTML & MonsterUI Complete Summary

###Let me create the data and code structure for you to run step by step:

```python
import fasthtml.common as ft
import monsterui.all as mui
from fastcore.all import *
import json
```

```python
dataset_dir = Path("Golden_Data_Set")
dataset_dir.mkdir(exist_ok=True)
```

```python
trace_example = {
    "request": {"messages": [{"role": "user", "content": "Hey! Need help with a pasta dish for tonight's potluck dinner - something that takes about an hour to make and NO seafood please (allergies in the group). Any ideas?"}]},
    "response": {"messages": [
        {"role": "system", "content": "You are an expert chef recommending delicious and useful recipes. Present only one recipe at a time. If the user doesn't specify what ingredients they have available, assume only basic ingredients are available."},
        {"role": "user", "content": "Hey! Need help with a pasta dish for tonight's potluck dinner - something that takes about an hour to make and NO seafood please (allergies in the group). Any ideas?"},
        {"role": "assistant", "content": "Absolutely! I recommend making a creamy mushroom and spinach tortellini bake – flavorful, comforting, and perfect for sharing at a potluck."}
    ]}
}
```

```python
for i in range(3):
    fname = f"trace_{20241201}_{120000 + i*1000}.json"
    (dataset_dir / fname).write_text(json.dumps(trace_example, indent=2))
```




### Basic HTML Elements
- `ft.Div()` - Basic container (plain HTML div)
- `ft.Li()` - List item 
- `ft.A()` - Link/anchor with `href` attribute
- `ft.Ul()` - Unordered list (bullet points)
- `ft.H1()`, `ft.H2()` - Headings
- `ft.P()` - Paragraph
- `ft.Button()` - Clickable button

### Special Elements
- `ft.Details()` + `ft.Summary()` - Collapsible dropdown section
- `mui.Container()` - Styled wrapper with spacing/centering
- `mui.render_md()` - Converts markdown to HTML

### CSS Classes for Chat UI
- `chat-bubble` - Basic speech bubble styling
- `chat-bubble-primary` - User messages (typically blue)
- `chat-bubble-secondary` - Assistant messages (typically gray)
- `chat` - Base chat container
- `chat-start` - Left-aligned bubbles
- `chat-end` - Right-aligned bubbles

### FastCore Path Operations
```python
dataset_dir = Path("Golden_Data_Set")
files = L(dataset_dir.glob("*.json"))  # Find JSON files
data = files[0].read_json()  # Read JSON directly
dt = files[0].stem  # Filename without extension
```

### Advanced FastCore Features
```python
globtastic(path, file_glob='*.json')  # Powerful file search
trs = globtastic(p, file_glob='*.json')
data = Path(trs[0]).read_json()
```

### Object Conversion
```python
from fastcore.basics import dict2obj, AttrDict, nested_idx
obj = dict2obj(data)  # Convert dict to object with dot notation
obj.response.messages[0].content  # Access with dots
nested_idx(data, ['response', 'messages', 0, 'content'])  # Deep access
```

### Flattening Nested Data
```python
def flatten_nested(d, parent_key='', sep='.'):
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_nested(v, new_key, sep).items())
    elif isinstance(d, list):
        for i, v in enumerate(d):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            items.extend(flatten_nested(v, new_key, sep).items())
    else:
        return {parent_key: d}
    return dict(items)

flat = flatten_nested(data)
contents = [v for k,v in flat.items() if k.endswith('content')]
```

### Chat Bubble Creation
```python
def chat_bubble(m):
    is_user = m["role"] == "user"
    if m["role"] == "system":
        return ft.Details(
            ft.Summary("System Prompt"),
            ft.Div(mui.render_md(m["content"]), cls="chat-bubble chat-bubble-secondary"),
            cls="chat chat-start"
        )
    return ft.Div(
        ft.Div(mui.render_md(m["content"]), 
               cls=f"chat-bubble {'chat-bubble-primary' if is_user else 'chat-bubble-secondary'}"),
        cls=f"chat {'chat-end' if is_user else 'chat-start'}"
    )

bubbles = data.response.messages.map(chat_bubble)
ft.Container(*bubbles)
```

### Navigation Logic
```python
files = L(globtastic(p, file_glob='*.json')).map(lambda x: Path(x).name)
files.sort()
current_idx = files.index('current_file.json')
next_file = files[current_idx + 1] if current_idx < len(files) - 1 else files[0]
prev_file = files[current_idx - 1] if current_idx > 0 else files[-1]
```

### Layout Components
```python
# Navigation bar
mui.DivFullySpaced(
    ft.A("← Previous", href="/prev"),
    ft.A("🏠 Home", href="/"),
    ft.A("Next →", href="/next"),
    cls="my-4"
)

# Two-column grid layout
mui.Grid(
    ft.Div(*bubbles),  # Left side - chat
    mui.Form(          # Right side - form
        mui.Select(*[ft.Option(code, value=code) for code in codes]),
        mui.TextArea("notes", rows=20),
        mui.Button("Save", type="submit")
    )
)
```

### Form Elements
```python
mui.Select(
    *[ft.Option(code, value=code) for code in ['bug', 'feature', 'error']],
    placeholder="Select option..."
)
mui.TextArea("Default text", name="notes", rows=5)
mui.Button("Save", type="submit")
```

### Complete Page Structure
```python
mui.Container(
    mui.H2("Page Title"),
    mui.DivFullySpaced(
        ft.A("Previous", href="/prev"),
        ft.A("Home", href="/"),
        ft.A("Next", href="/next")
    ),
    mui.Grid(
        ft.Div(*chat_bubbles),
        mui.Form(
            mui.Select(*options),
            mui.TextArea("", rows=20),
            mui.Button("Save")
        )
    )
)
```

### Data Structure Example
```python
trace_data = {
    "request": {"messages": [{"role": "user", "content": "Question"}]},
    "response": {"messages": [
        {"role": "system", "content": "System prompt"},
        {"role": "user", "content": "Question"},
        {"role": "assistant", "content": "Answer"}
    ]}
}
```

### Key Patterns
- HTML elements nest like boxes: `Container(Grid(Div(...), Form(...)))`
- Use `*` to unpack lists: `Select(*options)` not `Select(options)`
- FastCore's `L()` adds useful methods like `.map()`
- `dict2obj()` enables dot notation access
- Grid automatically creates responsive columns

