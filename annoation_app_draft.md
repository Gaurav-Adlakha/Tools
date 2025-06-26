**Setup:**
```python
import fasthtml.common as ft, json
import monsterui.all as mui
from fastcore.all import *
import fasthtml.common as ft
import monsterui.all as mui

from fasthtml.jupyter import render_ft
render_ft()

```
[Gist link](https://gist.github.com/Gaurav-Adlakha/c178fa5d646764040785b4d3c84c574b)

**Create test data:**
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
        {"role": "assistant", "content": "Absolutely! I recommend making a creamy mushroom and spinach tortellini bake – flavorful, comforting, and perfect for sharing at a potluck. It should take about an hour from start to finish."}
    ]}
}
```

```python
for i in range(3): (dataset_dir / f"trace_{20241201}_{120000 + i*1000}.json").write_text(json.dumps(trace_example, indent=2))
```

**Basic HTML Elements:**
```python
ft.Div("Basic container")
```

```python
ft.Li("List item")
```

```python
ft.A("Click me", href="/page")
```

```python
ft.Ul(ft.Li("Item 1"), ft.Li("Item 2"))
```

```python
ft.H1("Big heading")
```

```python
ft.P("Paragraph text")
```

```python
ft.Button("Click me")
```

**Special Elements:**
```python
ft.Details(ft.Summary("Click to expand"), ft.P("Hidden content"))
```

```python
mui.Container("Styled wrapper")
```

```python
mui.render_md("**Bold text** and *italic*")
```

**Chat Styling:**
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
```

```python
ft.Div(ft.Div("User message", cls="chat-bubble chat-bubble-primary"), cls="chat chat-end")
```

```python
ft.Div(ft.Div("Assistant message", cls="chat-bubble chat-bubble-secondary"), cls="chat chat-start")
```

**Path Operations:**
```python
files = L(dataset_dir.glob("*.json"))
files
```

```python
data = files[0].read_json()
data
```

```python
files[0].stem
```

**Advanced File Operations:**
```python
trs = globtastic(dataset_dir, file_glob='*.json')
trs
```

```python
Path(trs[0]).read_json()
```

**Object Conversion:**
```python
obj = dict2obj(trace_example)
obj.response.messages[0].content
```

```python
nested_idx(trace_example, ['response', 'messages', 0, 'content'])
```

**Flattening Data:**
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
```

```python
flat = flatten_nested(trace_example)
[v for k,v in flat.items() if k.endswith('content')]
```

**Chat Bubble Function:**
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
        ft.Div(mui.render_md(m["content"]), cls=f"chat-bubble {'chat-bubble-primary' if is_user else 'chat-bubble-secondary'}"),
        cls=f"chat {'chat-end' if is_user else 'chat-start'}"
    )
```

```python
data = dict2obj(trace_example)
bubbles = data.response.messages.map(chat_bubble)
ft.Container(*bubbles)
```

**Navigation Logic:**
```python
files = L(globtastic(dataset_dir, file_glob='*.json')).map(lambda x: Path(x).name).sorted()
current_idx = files.index('trace_20241201_120000.json')
next_file = files[current_idx + 1] if current_idx < len(files) - 1 else files[0]
prev_file = files[current_idx - 1] if current_idx > 0 else files[-1]
print(f"Current: {current_idx}, Next: {next_file}, Prev: {prev_file}")
```

**Layout Components:**
```python
mui.DivFullySpaced(
    ft.A("← Previous", href="/prev"),
    ft.A("🏠 Home", href="/"),
    ft.A("Next →", href="/next"),
    cls="my-4"
)
```

```python
mui.Grid(ft.Div("Left content"), ft.Div("Right content"))
```

**Form Elements:**
```python
sample_codes = ['bug', 'feature', 'error']
mui.Select(*[ft.Option(code, value=code) for code in sample_codes], placeholder="Select option...")
```

```python
mui.TextArea("Default text", name="notes", rows=5)
```

```python
mui.Button("Save", type="submit")
```

**Complete Form:**
```python
mui.Form(
    mui.Select(*[ft.Option(code, value=code) for code in sample_codes], placeholder="Select issue type..."),
    mui.TextArea("Sample annotation", rows=5),
    mui.Button("💾 Save", type="submit")
)
```

**Complete Page Layout:**
```python
sample_bubbles = [
    ft.Div(ft.Div("User: Hello!", cls="chat-bubble chat-bubble-primary"), cls="chat chat-end"),
    ft.Div(ft.Div("Assistant: Hi there!", cls="chat-bubble chat-bubble-secondary"), cls="chat chat-start")
]

mui.Container(
    mui.DivFullySpaced(
        ft.A("← Previous", href="/prev"),
        ft.A("🏠 Home", href="/"),
        ft.A("Next →", href="/next"),
        cls="my-4"
    ),
    mui.Grid(
        ft.Div(*sample_bubbles),
        mui.Form(
            mui.Select(*[ft.Option(code, value=code) for code in sample_codes], placeholder="Select issue type..."),
            mui.TextArea("Sample annotation", rows=5),
            mui.Button("💾 Save", type="submit")
        )
    )
)
```

**List Creation:**
```python
def list_traces():
    files = L(dataset_dir.glob("*.json")).sorted()
    return ft.Ul(*[ft.Li(ft.A(f"{f.stem}: {dict2obj(f.read_json()).request.messages[0].content[:60]}...", href=f"/annotate/{f.name}")) for f in files])
```

```python
list_traces()
```

**Complete Annotation Page:**
```python
def create_annotation_page(fname):
    data = dict2obj(Path(dataset_dir/fname).read_json())
    bubbles = data.response.messages.map(chat_bubble)
    files = L(dataset_dir.glob("*.json")).map(lambda x: x.name).sorted()
    current_idx = files.index(fname)
    next_file = files[current_idx + 1] if current_idx < len(files) - 1 else files[0]
    prev_file = files[current_idx - 1] if current_idx > 0 else files[-1]
    return mui.Container(
        mui.DivFullySpaced(
            ft.A("Previous", href=f"/annotate/{prev_file}"),
            ft.A("Home", href="/"),
            ft.A("Next", href=f"/annotate/{next_file}"),
            cls="my-4"
        ),
        mui.Grid(
            ft.Div(*bubbles),
            mui.Form(
                mui.Select(*[ft.Option(code, value=code) for code in ['bug', 'feature', 'error']], placeholder="Select coding..."),
                mui.TextArea("", name="notes", rows=20),
                mui.Button("Save", type="submit"),
                action=f"/save/{fname}", method="post"
            )
        )
    )
```

```python
create_annotation_page('trace_20241201_120000.json')
```

# orginal code
```python
import fasthtml.common as ft
import monsterui.all as mui
import os
import json
import glob

DATASET_DIR = os.path.join(os.path.dirname(__file__), "golden_dataset")

app, rt = mui.fast_app(hdrs=mui.Theme.blue.headers())

def list_traces():
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.json')]
    files.sort()  # Changed to sort in ascending order
    items = []
    for fname in files:
        path = os.path.join(DATASET_DIR, fname)
        with open(path) as f:
            data = json.load(f)
        msg = data["request"]["messages"][0]["content"]
        dt = fname.split('_')[1] + ' ' + fname.split('_')[2]
        has_open_coding = bool(data.get("open_coding", ""))
        has_axial_coding = bool(data.get("axial_coding_code", ""))
        check_mark = "✅ " if has_open_coding else ""
        check_mark += "✅ " if has_axial_coding else ""
        items.append(
            ft.Li(ft.A(f"{check_mark}{dt}: {msg[:60]}...", href=annotate.to(fname=fname), cls=mui.AT.classic))
        )
    return ft.Ul(*items, cls=mui.ListT.bullet)

@rt
def index():
    return mui.Container(
        mui.H2("Golden Dataset Traces"),
        list_traces()
    )

def chat_bubble(m):
    is_user = m["role"] == "user"
    if m["role"] == "system":
        return ft.Details(
            ft.Summary("System Prompt"),
            ft.Div(
                mui.render_md(m["content"]),
                cls="chat-bubble chat-bubble-secondary"
            ),
            cls="chat chat-start"
        )
    return ft.Div(
        ft.Div(
            mui.render_md(m["content"]),
            cls=f"chat-bubble {'chat-bubble-primary' if is_user else 'chat-bubble-secondary'}"
        ),
        cls=f"chat {'chat-end' if is_user else 'chat-start'}"
    )

def get_unique_open_coding_codes():
    codes = set()
    for fname in glob.glob(os.path.join(DATASET_DIR, '*.json')):
        with open(fname) as f:
            data = json.load(f)
        note = data.get('open_coding', '')
        if note and note.strip().lower() != 'n/a':
            # Split on double space or newlines for multiple codes, else treat as one code
            for code in note.split('\n'):
                code = code.strip()
                if code:
                    codes.add(code)
    return sorted(codes)

def get_unique_axial_coding_codes():
    codes = set()
    for fname in glob.glob(os.path.join(DATASET_DIR, '*.json')):
        with open(fname) as f:
            data = json.load(f)
        code = data.get('axial_coding_code', '')
        if code and code.strip():
            codes.add(code.strip())
    return sorted(codes)

@rt
def annotate(fname:str):
    path = os.path.join(DATASET_DIR, fname)
    with open(path) as f:
        data = json.load(f)
    chat =  data["response"]["messages"]
    bubbles = [chat_bubble(m) for m in chat]
    notes = data.get("open_coding", "")
    axial_code = data.get("axial_coding_code", "")
    axial_code_options = get_unique_axial_coding_codes()
    # Get next and previous files
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.json')]
    files.sort()  # Changed to sort in ascending order
    current_idx = files.index(fname)
    next_file = files[current_idx + 1] if current_idx < len(files) - 1 else files[0]
    prev_file = files[current_idx - 1] if current_idx > 0 else files[-1]
    return mui.Container(
        mui.DivFullySpaced(
            ft.A("Previous", href=annotate.to(fname=prev_file), cls=mui.AT.classic),
            ft.A("Home", href=index.to(), cls=mui.AT.classic),
            ft.A("Next", href=annotate.to(fname=next_file), cls=mui.AT.classic),
            cls="my-4"
        ),
        mui.Grid(
            ft.Div(*bubbles),
            mui.Form(
                mui.Select(
                    *[ft.Option(code, value=code) for code in axial_code_options],
                    id="axial_coding_code", icon=True, insertable=True, multiple=False,
                    value=axial_code, placeholder="Select or add axial coding (failure mode)..."
                ),
                mui.TextArea(notes, name="notes", value=notes, rows=20),
                mui.Button("Save", type="submit"),
                action=save_annotation.to(fname=fname), method="post",
                cls='w-full flex flex-col gap-2'
            ),
        ),
    )

@rt
def save_annotation(fname:str, notes:str, axial_coding_code:str=None):
    path = os.path.join(DATASET_DIR, fname)
    with open(path) as f:
        data = json.load(f)
    data["open_coding"] = notes
    if axial_coding_code is not None:
        data["axial_coding_code"] = axial_coding_code
    with open(path, "w") as f:
        json.dump(data, f)
    return ft.Redirect(annotate.to(fname=fname))

@rt
def theme():
    return mui.ThemePicker()

ft.serve()
```
