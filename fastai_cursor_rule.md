---
description: Fast.ai coding style and fastcore library patterns for concise, expressive Python code
globs: **/*.py, **/*.ipynb
alwaysApply: false
---

# Fast.ai Coding Style Rules

## Core Philosophy
- **Brevity facilitates reasoning** - Keep code concise but expressive
- **One complete idea per line** - Each line should implement one semantic concept
- **Domain expertise assumed** - Use standard abbreviations known in the field
- **Mathematical notation style** - Layout code similar to mathematical expressions
- **Functional programming preferred** - Use comprehensions, lambda, and functional patterns

## Symbol Naming Conventions

### Standard Python Casing
```python
# Classes: CamelCase
class DataLoader: pass

# Functions/variables: under_score
def load_data(): pass
data_path = "path/to/data"
```

### Domain-Specific Abbreviations
```python
# Computer Vision
sz = 224        # size
img = Image()   # image
tfm = Transform() # transform
coord = (10,20) # coordinate

# NLP
lm = LanguageModel()  # language model
tok = Tokenizer()     # tokenizer

# ML General
bs = 32           # batch size
lr = 1e-3         # learning rate
```

### Short Variable Names
```python
# Comprehensions and loops
o = [process(x) for x in items]  # object in comprehension
i = 0                            # index
k,v = key,value                  # dictionary items
x = tensor_input                 # tensor input to algorithm

# Following paper nomenclature
conv1 = nn.Conv2d()              # not first_convolutional_layer
kl_div = kl_divergence()         # not kullback_leibler_divergence
```

## Layout and Formatting

### Line Length and Structure
```python
# Up to 160 characters per line for modern screens
very_long_function_call(param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11, param12)

# One-line if statements
result = value if condition else default

# One-line function definitions when they fit
def square(x): return x**2
def is_valid(x): return x > 0 and x < 100
```

### Alignment for Conceptual Similarity
```python
# Align similar operations
train_ds = ImageDataLoaders.from_folder(path/'train', transforms=tfms)
valid_ds = ImageDataLoaders.from_folder(path/'valid', transforms=tfms)

# Constructor alignment with store_attr
class Model:
    def __init__(self, lr=1e-3, bs=32, epochs=5):
        store_attr()  # Auto-assigns all parameters
```

### Vertical Space Minimization
```python
# Import multiple modules on one line
from fastcore.all import *
from fastai.vision.all import Path,Image,PILImage

# Group related one-liners without blank lines
def relu(x): return torch.max(x, 0)
def sigmoid(x): return 1/(1+torch.exp(-x))
def tanh(x): return torch.tanh(x)

# Destructuring assignment without spaces after commas
self.lr,self.bs,self.epochs = lr,bs,epochs
```

### Mathematical Layout
```python
# Space equations like mathematical notation
loss = y_pred - y_true
mse  = (loss**2).mean()
mae  = loss.abs().mean()

# No spaces in paths (like shell notation)
path = Path.home()/'data'/'images'/'train'

# Group equation parts clearly
numerator   = torch.exp(logits - logits.max(dim=-1, keepdim=True)[0])
denominator = numerator.sum(dim=-1, keepdim=True)
softmax     = numerator / denominator
```

## Fastcore Library Patterns

### Class Construction with store_attr
```python
class DataLoader:
    def __init__(self, dataset, batch_size=32, shuffle=True, num_workers=0):
        store_attr()  # Automatically assigns all parameters to self
    
    # Add clean repr
    __repr__ = basic_repr('dataset,batch_size,shuffle')
```

### Method Addition with @patch
```python
# Add methods to existing classes
@patch
def accuracy(self:Learner):
    "Calculate accuracy for current model"
    return (self.preds.argmax(dim=1)==self.targets).float().mean()

# Patch with delegation
@patch
@delegates(plt.show)
def show(self:Image, **kwargs):
    "Display image with matplotlib"
    plt.imshow(self.data)
    plt.show(**kwargs)
```

### Delegation with @delegates
```python
# Avoid **kwargs API problems
def train_model(lr, epochs, model_cls=ResNet):
    return model_cls(lr=lr, epochs=epochs)

@delegates(train_model)
def fit(data, **kwargs):
    "Train model with proper signature forwarding"
    model = train_model(**kwargs)
    return model.fit(data)
```

### Enhanced Lists with L
```python
# Use L instead of list for enhanced functionality
files = L(path.glob('*.jpg'))
sizes = files.map(lambda x: x.stat().st_size)
large_files = files.filter(lambda x: x.stat().st_size > 1000000)

# Indexing with lists and boolean masks
first_three = files[:3]
selected = files[[0,2,4]]
large_only = files[sizes > 1000000]
```

### Delegation with GetAttr
```python
class Model(GetAttr):
    _default = 'backbone'  # Delegate to self.backbone
    
    def __init__(self, backbone):
        self.backbone = backbone
        self.head = nn.Linear(512, 10)
    
    def forward(self, x):
        # Can call backbone methods directly on Model
        features = self.extract_features(x)  # Calls self.backbone.extract_features
        return self.head(features)
```

### Functional Programming Patterns
```python
# Use comprehensions over loops
squares = [x**2 for x in range(10)]
filtered = [x for x in items if x.is_valid()]
mapped = {k:process(v) for k,v in data.items()}

# Curried functions for partial application
def add(a,b): return a+b
add5 = partial(add, 5)
results = L(items).map(add5)

# Compose operations
pipeline = compose(normalize, resize, to_tensor)
processed = pipeline(image)
```

### Testing Patterns
```python
# Use test_eq for assertions
def test_model_output():
    model = SimpleModel()
    input_tensor = torch.randn(1, 3, 224, 224)
    output = model(input_tensor)
    test_eq(output.shape, torch.Size([1, 10]))
    
# Test with expected output shown
def test_accuracy():
    preds = torch.tensor([0.1, 0.8, 0.1])
    targs = torch.tensor([1])
    test_eq(accuracy(preds, targs), 0.8)  # Shows expected result
```

### Configuration and Utilities
```python
# AttrDict for configuration
config = AttrDict({
    'lr': 1e-3,
    'bs': 32,
    'epochs': 10
})
# Access as attributes or dict
print(config.lr)    # 1e-3
print(config['bs']) # 32

# Parallel processing
def process_item(item):
    return expensive_operation(item)

results = parallel(process_item, items, n_workers=4)
```

## Algorithm Implementation

### Performance and Broadcasting
```python
# Use broadcasting instead of loops
# Bad:
# result = []
# for i in range(len(x)):
#     result.append(x[i] * weights[i])

# Good:
result = x * weights  # Broadcasting

# Advanced indexing over specialized methods
selected = tensor[mask]           # not tensor.masked_select(mask)
gathered = tensor[indices]        # not tensor.gather(dim, indices)
```

### Paper Implementation
```python
def attention(q, k, v, mask=None):
    "Multi-head attention from 'Attention Is All You Need' (Eq. 1)"
    # Equation reference from paper
    d_k = q.size(-1)
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)  # Eq. 1
    if mask is not None: scores.masked_fill_(mask == 0, -1e9)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, v)
```

### Lazy Data Handling
```python
def data_generator(path):
    "Generate data lazily for large datasets"
    for file in path.glob('*.jpg'):
        yield load_and_process(file)

# Use generators for memory efficiency
dataset = (transform(item) for item in data_generator(data_path))
```

## Import and Module Organization

### Liberal Imports
```python
# Import everything when using most of a module
from fastcore.all import *
from fastai.vision.all import *
from torch.nn.functional import *

# Avoid long import lists for commonly used modules
import numpy as np  # Only if not importing everything
```

### __all__ Definition
```python
# Define what gets exported
__all__ = ['Model', 'train', 'predict', 'accuracy']
```

## Documentation Style

### Concise Docstrings
```python
def accuracy(preds, targs):
    "Percentage of correct predictions"
    return (preds.argmax(dim=-1)==targs).float().mean()

def train_model(data, lr=1e-3, epochs=5):
    "Train model on `data` with `lr` for `epochs`"
    # Implementation here
```

### Paper References
```python
def transformer_block(x, n_heads=8):
    "Transformer block from 'Attention Is All You Need' https://arxiv.org/abs/1706.03762"
    attention_out = multi_head_attention(x, n_heads)  # Section 3.2.2
    return layer_norm(attention_out + x)              # Equation 5
```

## Common Anti-Patterns to Avoid

### Don't Use Auto-formatters
```python
# Fastai style maintains domain-specific formatting
# Don't run autopep8, yapf, or black
```

### Avoid Verbose Naming
```python
# Bad:
def calculate_mean_squared_error_loss(predictions, targets):
    pass

# Good:
def mse_loss(preds, targs):
    pass
```

### Don't Separate Simple Operations
```python
# Bad:
x = input_tensor
x = self.conv1(x)
x = F.relu(x)

# Good:
x = F.relu(self.conv1(input_tensor))
```

### Avoid Unnecessary Abstractions
```python
# Bad: Over-abstracted
class DataProcessor:
    def process(self, data):
        return self.transform(self.normalize(self.resize(data)))

# Good: Direct and clear
def process(data): return transform(normalize(resize(data)))
```

## Integration with Modern Python

### Use Latest Features
```python
# f-strings for formatting
msg = f'Epoch {epoch}: loss={loss:.4f}, acc={acc:.2%}'

# Pathlib for paths
data_path = Path.home()/'datasets'/'imagenet'
model_path = Path('models')/'resnet50.pkl'

# Type hints where helpful
def train(model: nn.Module, data: DataLoader) -> dict:
    pass
```

### Leverage Python 3.6+ Features
```python
# Dict comprehensions with f-strings
metrics = {f'{k}_loss': v for k,v in losses.items()}

# Generator expressions for memory efficiency
processed = (transform(x) for x in large_dataset)
```
