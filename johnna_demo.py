from fasthtml.common import * # type: ignore
import json

app, rt = fast_app(live=True, static_path="images", hdrs=[ # type: ignore
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
])

# Load dataset metadata
with open('dataset_metadata.json', 'r') as f:
    dataset = json.load(f)

# Session state for current image index
current_index = 0

@rt
def index():
    return get_image_page(0)

@rt
def image(idx: int):
    return get_image_page(idx)

@rt("/next/{idx}")
def next_image(idx: int):
    new_idx = (idx + 1) % len(dataset)
    return get_image_page(new_idx)

@rt("/prev/{idx}")
def prev_image(idx: int):
    new_idx = (idx - 1) % len(dataset)
    return get_image_page(new_idx)

def get_image_page(idx):
    if idx < 0 or idx >= len(dataset):
        idx = 0
    
    item = dataset[idx]
    
    return (
        Title("Species Identification Viewer"),
        Container(
            H1("Species Identification Dataset"),
            Article(
                Header(H2(f"Image {idx + 1} of {len(dataset)}")),
                Div(
                    Img(src=f"/{item['image_file']}", 
                        alt=f"Species observation {item['observation_id']}",
                        style="max-width: 100%; height: auto; border-radius: 8px;"),
                    style="text-align: center; margin: 20px 0;"
                ),
                Div(
                    H3("Metadata"),
                    P(Strong("Observation ID: "), item['observation_id']),
                    P(Strong("Answer: "), item['answer']),
                    P(Strong("Correct Species: "), item.get('correct_species', 'Unknown')),
                    Details(
                        Summary("Species Options"),
                        Ul(*[
                            Li(
                                option, 
                                style="color: green; font-weight: bold;" if i == item['answer'] else ""
                            ) for i, option in enumerate(item['options'])
                        ])
                    ),
                    style="background: var(--pico-card-background-color); padding: 1rem; border-radius: 8px; margin: 20px 0;"
                ),
                Footer(
                    Div(
                        A("← Previous", href=f"/prev/{idx}", role="button", cls="secondary"),
                        Span(f"{idx + 1} / {len(dataset)}", style="margin: 0 20px; align-self: center;"),
                        A("Next →", href=f"/next/{idx}", role="button"),
                        style="display: flex; justify-content: space-between; align-items: center;"
                    )
                )
            )
        )
    )

serve()
