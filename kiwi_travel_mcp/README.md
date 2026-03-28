# Kiwi Travel MCP 🥝✈️

## Overview
A specialized notebook-based MCP system demonstrating agentic flows with LangGraph for travel planning and itinerary management. This project showcases multi-agent orchestration, tool integration, and complex workflow automation.

## Features
- **Travel Planning**: End-to-end itinerary management
- **Multi-Agent Coordination**: Multiple agents working together
- **LangGraph Integration**: State machine based flows
- **Dynamic Routing**: Intelligent agent selection
- **Real-time Updates**: Live itinerary modifications
- **Constraint Management**: Handle travel restrictions and preferences

## Architecture

```
Travel Agent System
├── Trip Planner Agent
│   ├── Flight Booking
│   ├── Hotel Reservation
│   └── Itinerary Builder
├── Flight Search Agent
│   ├── Price Comparison
│   ├── Availability Check
│   └── Route Optimization
├── Activity Recommendation Agent
│   ├── Destination Info
│   ├── Activity Search
│   └── Rating Analysis
└── Cost Optimization Agent
    ├── Budget Tracking
    ├── Deal Finder
    └── Expense Management
```

## Notebook Contents

### Tutorial 6: Agentic Flows with LangGraph V2
**Location**: `Tutorial_6_Agentic_flows_with_Langgraph_V2_final.ipynb`

#### Sections:
1. **Introduction to LangGraph**
   - State graphs
   - Conditional edges
   - Tool calling

2. **Multi-Agent Architecture**
   - Agent definition
   - Tool definitions
   - Agent coordination

3. **Travel Planning Workflow**
   - Trip parsing
   - Agent routing
   - State management

4. **Implementation Details**
   - Code patterns
   - Error handling
   - Testing strategies

## Setup & Usage

### Installation
```bash
# Install dependencies
pip install langgraph langchain python-dotenv

# Jupyter kernel
jupyter notebook
```

### Configuration
Set environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export SERPAPI_API_KEY="..."  # For travel searches
export GOOGLE_MAPS_API_KEY="..."
```

### Running the Notebook
```bash
jupyter notebook Tutorial_6_Agentic_flows_with_Langgraph_V2_final.ipynb
```

## Key Concepts

### State Definition
```python
class TripState(TypedDict):
    destination: str
    start_date: date
    end_date: date
    budget: float
    preferences: dict
    flights: list
    hotels: list
    activities: list
    itinerary: str
```

### Agent Definition
```python
class TravelAgent:
    def __init__(self, name, role, tools):
        self.name = name
        self.role = role
        self.tools = tools
    
    async def process(self, state):
        # Agent logic
        pass
```

### Workflow Graph
```python
workflow = StateGraph(TripState)

# Add nodes
workflow.add_node("plan", plan_node)
workflow.add_node("search", search_node)
workflow.add_node("book", book_node)

# Add edges
workflow.add_edge("plan", "search")
workflow.add_conditional_edges("search", route_to_booking)
```

## Tools Available

### Flight Tools
- `search_flights(origin, destination, dates)` - Find flights
- `get_flight_details(flight_id)` - Get flight info
- `book_flight(flight_id, passengers)` - Book flight
- `calculate_flight_cost(flight_id)` - Get pricing

### Hotel Tools
- `search_hotels(city, dates)` - Find accommodations
- `get_Hotel_details(hotel_id)` - Hotel information
- `book_hotel(hotel_id, dates)` - Reserve hotel
- `get_hotel_reviews(hotel_id)` - Read reviews

### Activity Tools
- `get_attractions(destination)` - Popular attractions
- `search_activities(location)` - Adventure activities
- `get_activity_reviews(activity_id)` - User reviews
- `recommend_activities(preferences)` - Smart recommendations

### Cost Management Tools
- `calculate_total_cost(components)` - Budget calculation
- `find_deals(destination, budget)` - Cost optimization
- `compare_options(options)` - Price comparison
- `track_expenses(items)` - Expense tracking

## Workflow Examples

### Simple Trip Planning
```
User: "Plan a 5-day trip to Paris for $2000"
    ↓
Trip Planner Agent
    ├─ Parse: Paris, 5 days, $2000 budget
    ├─ Call Flight Search Agent
    ├─ Call Hotel Search Agent
    ├─ Call Activity Recommendation Agent
    ├─ Check Budget Constraints
    └─ Return Optimized Itinerary
```

### Multi-Agent Coordination
```
Complex Request:
"Plan a tech conference trip with activities"
    ↓
Primary Planner
    ├─ Route to: Flight Agent
    ├─ Route to: Hotel Agent
    ├─ Route to: Activity Agent (Tech venues)
    ├─ Route to: Cost Optimization Agent
    └─ Synthesize final itinerary
```

## LangGraph Patterns

### Conditional Routing
```python
def should_book(state):
    if state["budget_approved"]:
        return "book"
    else:
        return "adjust"

workflow.add_conditional_edges(
    "review",
    should_book,
    {"book": "booking", "adjust": "planning"}
)
```

### Sub-Graphs
```python
# Flight booking subgraph
flight_graph = StateGraph(FlightState)
flight_graph.add_node("search", search_flights)
flight_graph.add_node("book", book_flight)

# Add to main graph
workflow.add_node("flight_workflow", flight_graph.compile())
```

### Error Handling
```python
def handle_error(state):
    if state["error"]:
        # Retry or escalate
        return "retry"
    return "continue"
```

## Resource Files

### Resources Directory
Contains:
- Sample itineraries
- Configuration templates
- Test data
- Example outputs

## Use Cases
- Travel agencies
- Tour operators
- Travel planning apps
- Corporate travel management
- Multi-destination optimization
- Budget-constrained planning
- Group travel coordination

## Performance Optimization

### Parallel Agent Calls
```python
# Run multiple agents in parallel
results = await asyncio.gather(
    flight_agent.process(state),
    hotel_agent.process(state),
    activity_agent.process(state)
)
```

### Caching
```python
# Cache flight searches
cache_key = f"{origin}_{destination}_{date}"
if cache_key in flight_cache:
    return flight_cache[cache_key]
```

## Testing

### Unit Tests
```python
async def test_flight_search():
    agent = FlightAgent()
    results = await agent.search("JFK", "CDG", "2024-06-01")
    assert len(results) > 0
```

### Integration Tests
```python
async def test_full_trip_planning():
    state = TripState(...)
    workflow = build_workflow()
    result = await workflow.invoke(state)
    assert result["itinerary"] is not None
```

## Advanced Features

### Real-Time Updates
```python
# Stream itinerary updates
async for update in workflow.stream(state):
    print(f"Update: {update}")
```

### Constraint Handling
```python
# Add constraints
constraints = {
    "max_flight_hours": 4,
    "min_hotel_rating": 4.0,
    "dietary_restrictions": ["vegetarian"]
}

state["constraints"] = constraints
```

### Personalization
```python
# User preferences
preferences = {
    "travel_style": "luxury",
    "pace": "relaxed",
    "activities": ["culture", "food", "adventure"]
}

state["preferences"] = preferences
```

## Monitoring & Debugging

### Execution Tracing
```python
# Trace agent decisions
for step in workflow.get_trace():
    print(f"Step: {step['node']}, State: {step['state']}")
```

### Performance Metrics
```python
# Track execution time
start = time.time()
result = await workflow.invoke(state)
duration = time.time() - start
print(f"Itinerary generated in {duration:.2f}s")
```

## Dependencies
- langgraph
- langchain
- python-dotenv
- httpx (for API calls)

## Best Practices
1. Define clear state boundaries
2. Use conditional routing appropriately
3. Handle agent errors gracefully
4. Cache expensive operations
5. Validate constraints early
6. Test agent interactions
7. Monitor performance
8. Document workflows

## Troubleshooting

### Agent Not Responding
- Check API keys
- Verify tool availability
- Review error logs
- Test agent independently

### State Issues
- Validate state schema
- Check edge conditions
- Review conditional logic
- Debug state transitions

### Performance Issues
- Profile slow operations
- Implement caching
- Parallelize agent calls
- Optimize tool definitions

## Future Enhancements
- [ ] Real-time price monitoring
- [ ] Machine learning recommendations
- [ ] Integration with booking APIs
- [ ] Multi-language support
- [ ] Advanced constraint solving
- [ ] Group coordination
- [ ] Sustainability scoring

## Resources
- LangGraph Docs: https://langchain-ai.github.io/langgraph
- LangChain: https://python.langchain.com
- Travel APIs: OpenTravelAPI, Skyscanner, Google Flights

## License & Attribution
Part of the Agent Development Kit examples and tutorials
