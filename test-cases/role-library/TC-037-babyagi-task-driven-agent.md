# TC-037: BabyAGI - Task-Driven Autonomous Agent

## Metadata
- **Source Project**: BabyAGI (yoheinakajima/babyagi)
- **GitHub**: github.com/yoheinakajima/babyagi
- **License**: MIT
- **Artifact Type**: Task-driven autonomous agent framework
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction at commit fa8930ebe72a82e5ad57b356e7cbec96290e5bb2
- **Scope**: BabyAGI classic autonomous agent; task-driven execution loop with built-in prompts

---

## Project Overview

BabyAGI is one of the pioneering **task-driven autonomous agent frameworks**. It uses a simple but powerful loop: create tasks, prioritize them, and execute them one by one. The framework is built on Flask with the Functionz framework for function orchestration.

### Key Characteristics
- **Task-driven execution**: Tasks are created, prioritized, and executed in a loop
- **Function-based architecture**: Uses Functionz framework for function registration
- **Auto-loading function packs**: Default AI and OS functions loaded automatically
- **Dynamic function discovery**: Functions can be called by name via module attributes

---

## Agent Framework Core

### 1. Module Initialization

```python
# babyagi/__init__.py

from flask import Flask, g
from .functionz.core.framework import Functionz
from .dashboard import create_dashboard
from .api import create_api_blueprint
import os
import importlib.util
import traceback
import sys

# Singleton instance of the functionz framework
_func_instance = Functionz()


def get_func_instance():
    return _func_instance

def create_app(dashboard_route='/dashboard'):
    app = Flask(__name__)

    # Remove leading slash if present to avoid double slashes
    if dashboard_route.startswith('/'):
        dashboard_route = dashboard_route[1:]

    # Create and register the dashboard blueprint with dashboard_route
    dashboard_blueprint = create_dashboard(_func_instance, dashboard_route)

    # Create and register the API blueprint
    api_blueprint = create_api_blueprint()

    # Register the blueprints
    app.register_blueprint(dashboard_blueprint, url_prefix=f'/{dashboard_route}')
    app.register_blueprint(api_blueprint)  # Mounted at '/api' as defined in the blueprint

    # Store the dashboard route for use in templates
    app.config['DASHBOARD_ROUTE'] = dashboard_route

    # Ensure the Functionz instance is accessible in the request context
    @app.before_request
    def set_functionz():
        g.functionz = _func_instance
        g.dashboard_route = dashboard_route  # Optional, if needed globally

    return app
```

### 2. Function Registration

```python
# Function to register functions using the babyagi framework
def register_function(*args, **kwargs):
    def wrapper(func):
        try:
            _func_instance.register_function(*args, **kwargs)(func)
            setattr(sys.modules[__name__], func.__name__, func)
            #print(f"Function '{func.__name__}' registered successfully.")
        except Exception as e:
            print(f"Error registering function '{func.__name__}': {e}")
            traceback.print_exc()
        return func
    return wrapper

# Function to load additional function packs
def load_functions(pack_name_or_path):
    #print(f"Attempting to load function pack: {pack_name_or_path}")
    if os.path.exists(pack_name_or_path):
        try:
            spec = importlib.util.spec_from_file_location("custom_pack", pack_name_or_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            #print(f"Custom pack loaded from {pack_name_or_path}")
        except Exception as e:
            #print(f"Failed to load custom pack from path '{pack_name_or_path}': {e}")
            traceback.print_exc()
    else:
        try:
            print(f"Assuming '{pack_name_or_path}' is an internal pack...")
            _func_instance.load_function_pack(pack_name_or_path)
            print(f"Internal pack '{pack_name_or_path}' loaded successfully.")
        except Exception as e:
            print(f"Failed to load internal pack '{pack_name_or_path}': {e}")
            traceback.print_exc()
```

### 3. Dynamic Function Invocation

```python
def __getattr__(name):
    """
    Dynamic attribute access for the babyagi module.
    If a function with the given name exists in the database,
    return a callable that executes the function via the executor.
    """
    try:
        if _func_instance.get_function(name):
            # Return a callable that executes the function via the executor
            return lambda *args, **kwargs: _func_instance.executor.execute(name, *args, **kwargs)
    except Exception as e:
        pass
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
```

### 4. Auto-Loading Function Packs

```python
# Auto-load default function packs when babyagi is imported
try:
    print("Attempting to load default function packs...")
    # Uncomment if needed
    _func_instance.load_function_pack('default/default_functions')
    _func_instance.load_function_pack('default/ai_functions')
    _func_instance.load_function_pack('default/os')
    _func_instance.load_function_pack('default/function_calling_chat')
except Exception as e:
    print(f"Error loading default function packs: {e}")
    traceback.print_exc()

print("babyagi/__init__.py loaded")
```

---

## Default Function Packs

| Pack | Purpose |
|------|---------|
| default_functions | Core utility functions |
| ai_functions | AI-related operations |
| os | Operating system utilities |
| function_calling_chat | Chat with function calling |

---

## Architecture Pattern

### Task Execution Loop

```
User Goal -> Task Creation -> Task Prioritization -> Task Execution -> Result
    ^                                                              |
    |                                                              v
    +-------------------- New Tasks Created ----------------------+
```

### Component Structure

```
babyagi/
├── __init__.py           # Main module with Functionz integration
├── api/                  # REST API endpoints
├── dashboard/            # Web UI dashboard
├── functionz/            # Core framework
│   └── core/
│       └── framework.py  # Function orchestration
└── default/              # Default function packs
    ├── default_functions/
    ├── ai_functions/
    ├── os/
    └── function_calling_chat/
```

---

## Evaluation Dimensions

### 1. Framework Simplicity
- [ ] Core logic is easy to understand
- [ ] Minimal dependencies for core functionality
- [ ] Clear separation between framework and functions

### 2. Function Registration
- [ ] Decorator-based registration is intuitive
- [ ] Dynamic function discovery works reliably
- [ ] Error handling for registration failures

### 3. Extensibility
- [ ] New function packs can be loaded
- [ ] Custom packs from file paths supported
- [ ] Internal packs have clear naming

### 4. API Design
- [ ] Flask blueprints for modular routes
- [ ] Dashboard route configurable
- [ ] Request context provides function access

### 5. Task Management
- [ ] Task creation mechanism
- [ ] Task prioritization logic
- [ ] Execution tracking

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Framework Simplicity | 25% | | |
| Function Registration | 20% | | |
| Extensibility | 20% | | |
| API Design | 15% | | |
| Task Management | 20% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Function Registration Tests
1. Test decorator-based registration
2. Verify function discovery via `__getattr__`
3. Test error handling on registration failure

### Function Pack Tests
1. Load default function packs
2. Load custom pack from file path
3. Test internal pack loading

### API Tests
1. Access dashboard route
2. Execute function via API
3. Test blueprint registration

### Task Execution Tests
1. Create and execute single task
2. Test task prioritization
3. Verify new task creation from results

---

## Notes

- BabyAGI pioneered the task-driven autonomous agent pattern
- Functionz framework provides function orchestration
- Flask-based design allows easy web integration
- Dynamic function discovery enables runtime extensibility
- MIT license allows full examination and modification
- Demonstrates simple but effective agent architecture
- Good reference for understanding agent framework fundamentals