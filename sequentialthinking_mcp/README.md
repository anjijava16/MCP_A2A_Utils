# Sequential Thinking MCP 🧠

## Overview
An MCP implementation for multi-step reasoning and sequential thought processes. This server enables agents to break down complex problems into step-by-step chains of reasoning and execution.

## Features
- **Step-by-Step Reasoning**: Break problems into sequences
- **Thought Chains**: Build reasoning chains
- **State Management**: Track reasoning state
- **Dependency Tracking**: Manage step dependencies
- **Result Synthesis**: Combine results across steps

## Architecture

```
User Query
    ↓
[Analyze Problem]
    ↓
Step 1: Initial Assessment
    ↓
Step 2: Data Gathering
    ↓
Step 3: Analysis
    ↓
Step 4: Synthesis
    ↓
Final Answer
```

## Tools Available
- `start_thinking(problem)` - Begin sequential thinking
- `step(description)` - Add reasoning step
- `track_state()` - Get current state
- `synthesize_result()` - Combine conclusions

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp
```

### Running
```bash
python sequential_thinking_mcp.py
```

## Example Workflow

### Problem Solving
```python
# Start thinking about complex problem
thinking = start_thinking("How to optimize database queries?")

# Step 1: Analyze current state
step("Analyze current query patterns and performance")

# Step 2: Identify bottlenecks
step("Identify slow queries and indexes missing")

# Step 3: Design solution
step("Design indexing strategy and query rewrites")

# Step 4: Implement
step("Implement changes and benchmark")

# Get result
result = synthesize_result()
```

## Use Cases
- Complex problem solving
- Research tasks
- Multi-step analysis
- Educational explanations
- Reasoning through complex topics

## Dependencies
- fastmcp
- mcp

## Performance Optimization
- State caching
- Efficient tracking
- Minimal overhead

## Best Practices
1. Clear step descriptions
2. Track dependencies
3. Manage state efficiently
4. Document reasoning
5. Validate outputs
