# Run Code MCP Server ⚙️

## Overview
An MCP server that enables safe, sandboxed code execution. This server allows agents to write, test, and execute code snippets in controlled environments with proper error handling and resource limits.

## Features
- **Code Execution**: Execute Python, JavaScript, shell commands
- **Sandboxing**: Isolated execution environment
- **Resource Limits**: CPU, memory, timeout constraints
- **Output Capture**: Capture stdout/stderr
- **Error Handling**: Detailed error reporting
- **Environment Support**: Multiple language runtimes

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp
# For additional language support
pip install docker  # For containerized execution
```

### Configuration
```bash
export CODE_EXECUTION_TIMEOUT=30
export MAX_MEMORY_MB=512
export ALLOWED_LANGUAGES="python,javascript,bash"
```

### Running
```bash
python run_code_server.py
```

## Tools Available

### Python Execution
- `run_python(code)` - Execute Python code
- `run_python_script(path)` - Run Python script
- `get_python_version()` - Check Python version

### JavaScript Execution
- `run_javascript(code)` - Execute JavaScript
- `run_javascript_file(path)` - Run JS file
- `get_node_version()` - Check Node.js version

### Shell Execution
- `run_shell_command(command)` - Execute shell
- `run_bash_script(path)` - Run bash script

### Code Management
- `create_code_file(path, code)` - Create file
- `test_code(code)` - Run tests
- `get_execution_history()` - View history

## Code Execution Examples

### Python Code
```python
# Run Python code
result = run_python("""
import math

def calculate_circle_area(radius):
    return math.pi * radius ** 2

area = calculate_circle_area(5)
print(f"Area: {area}")
""")

# Returns:
# {
#   "output": "Area: 78.53981633974483",
#   "error": None,
#   "execution_time": 0.05
# }
```

### JavaScript Code
```python
result = run_javascript("""
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

console.log(fibonacci(10));
""")
```

### Shell Commands
```python
result = run_shell_command("ls -la /tmp")

# Returns file listing in output
```

## Sandboxing Strategy

### Container-Based Isolation
```python
# Docker-based execution (optional)
USE_DOCKER = True

# Execution runs in isolated container
# - Separate filesystem
# - Limited network access
# - Resource constraints
# - No host system access
```

### Timeout Management
```python
# Prevent infinite loops
EXECUTION_TIMEOUT = 30  # seconds

# Execution terminates after timeout
# Returns: TimeoutError
```

### Resource Limits
```python
# Memory limits
MAX_MEMORY = 512  # MB

# CPU limits
CPU_LIMIT = 1  # CPU cores

# File size limits
MAX_FILE_SIZE = 100  # MB
```

## Error Handling

### Syntax Errors
```python
result = run_python("this is not valid python")
# Returns:
# {
#   "output": "",
#   "error": "SyntaxError: ...",
#   "execution_time": 0.01
# }
```

### Runtime Errors
```python
result = run_python("x = 1 / 0")
# Returns:
# {
#   "output": "",
#   "error": "ZeroDivisionError: ...",
#   "execution_time": 0.05
# }
```

### Timeout
```python
result = run_python("while True: pass", timeout=5)
# Returns:
# {
#   "output": "",
#   "error": "TimeoutError: Execution timed out",
#   "execution_time": 5.0
# }
```

## Advanced Features

### Multi-Language Execution
```python
# Python creates data
python_result = run_python("data = [1, 2, 3, 4, 5]")

# Write to file
create_code_file("data.json", json.dumps(python_result))

# JavaScript processes
js_result = run_javascript("""
const data = require('./data.json');
const doubled = data.map(x => x * 2);
console.log(doubled);
""")
```

### Code Testing
```python
# Write and test code
code = """
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    print("All tests passed!")

test_add()
"""

result = test_code(code)
# Runs tests and reports results
```

### Execution History
```python
# Get history of executions
history = get_execution_history()

for execution in history:
    print(f"Code: {execution['code'][:50]}...")
    print(f"Status: {execution['status']}")
    print(f"Time: {execution['execution_time']}s")
```

## Use Cases
- Educational coding environments
- Algorithm testing
- Data analysis
- Code generation verification
- Script execution
- Testing during development

## Security Considerations

### Input Validation
```python
# Validate code before execution
def validate_code(code):
    # Check for dangerous patterns
    forbidden = ['__import__', 'eval', 'exec']
    for pattern in forbidden:
        if pattern in code:
            raise SecurityError(f"Pattern {pattern} not allowed")
```

### Execution Isolation
```python
# Each execution is isolated
# - Separate namespace
# - No access to other executions
# - Limited filesystem access
```

### No Network Access
```python
# By default, no network
# Code cannot:
# - Make HTTP requests
# - Connect to databases
# - Access external APIs
```

## Performance Optimization

### Caching
```python
# Cache frequently executed code
code_hash = hash(code)
if code_hash in execution_cache:
    return execution_cache[code_hash]
```

### Parallel Execution
```python
# Execute multiple independent snippets in parallel
results = await asyncio.gather(
    run_python(code1),
    run_python(code2),
    run_python(code3)
)
```

## Configuration Options

### Language Support
```python
SUPPORTED_LANGUAGES = {
    "python": True,
    "javascript": True,
    "bash": True,
    "ruby": False,
    "rust": False
}
```

### Execution Settings
```python
EXECUTION_CONFIG = {
    "timeout": 30,
    "max_memory": 512,
    "working_directory": "/tmp",
    "environment_variables": {},
    "use_docker": False
}
```

## Testing

### Unit Tests
```python
@pytest.mark.asyncio
async def test_python_execution():
    result = run_python("print('hello')")
    assert "hello" in result["output"]

@pytest.mark.asyncio
async def test_timeout():
    result = run_python("while True: pass", timeout=1)
    assert "TimeoutError" in result["error"]
```

## Dependencies
- fastmcp
- mcp
- docker (optional, for Docker support)
- Various language runtimes (Python, Node.js, Bash)

## Best Practices
1. Implement strict sandboxing
2. Set appropriate timeouts
3. Limit resource usage
4. Validate all code input
5. Log execution details
6. Handle errors gracefully
7. Monitor execution metrics
8. Implement access controls

## Troubleshooting

### Code Not Executing
- Check language support
- Verify syntax
- Check timeout settings
- Review error messages

### Resource Issues
- Reduce memory limit
- Set shorter timeout
- Optimize code
- Use simpler operations

## Future Enhancements
- [ ] Additional language support
- [ ] Advanced debugging
- [ ] Performance profiling
- [ ] Code quality analysis
- [ ] Interactive REPL
- [ ] Distributed execution
