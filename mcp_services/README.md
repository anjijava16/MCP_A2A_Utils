# MCP Services 🎯

## Overview
A collection of higher-level MCP service implementations that build on top of the core MCP framework. This folder contains production-ready services that provide complete functionality for specific domains and use cases.

## Features
- **Service-Oriented Architecture**: Complete services with API boundaries
- **Business Logic Integration**: Domain-specific implementations
- **Configuration Management**: Environment-based configuration
- **Logging & Monitoring**: Built-in observability
- **Error Handling**: Comprehensive error management
- **Performance Optimization**: Caching and optimization strategies

## Services

### MCP Service Base
**Purpose**: Foundation for all service implementations

**Components:**
- Service lifecycle management
- Configuration loading
- Error handling framework
- Logging setup
- Health checks

**Usage:**
```python
from mcp_services import MCPService

class WeatherService(MCPService):
    def __init__(self, config):
        super().__init__(config)
        self.api_client = WeatherAPI()
    
    async def get_weather(self, location):
        return await self.api_client.get(location)
```

## Service Types

### API Services
**Purpose**: Wrap external APIs as MCP services

**Examples:**
- Weather API service
- Stock market service
- News aggregator service
- Search service

**Implementation Pattern:**
```python
class APIService(MCPService):
    def __init__(self, config):
        super().__init__(config)
        self.base_url = config["api_url"]
        self.api_key = config["api_key"]
    
    async def make_request(self, endpoint, params):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        return await self.http_client.get(url, headers=headers, params=params)
```

### Database Services
**Purpose**: Provide database abstraction layer

**Examples:**
- SQL database service
- NoSQL service
- Cache service
- Data warehouse service

**Implementation Pattern:**
```python
class DatabaseService(MCPService):
    def __init__(self, config):
        super().__init__(config)
        self.db_connection = self.connect_database()
    
    async def query(self, sql, params):
        return await self.db_connection.execute(sql, params)
    
    async def close(self):
        await self.db_connection.close()
```

### Business Logic Services
**Purpose**: Implement business rules and workflows

**Examples:**
- Order processing service
- User authentication service
- Payment processing service
- Report generation service

**Implementation Pattern:**
```python
class BusinessService(MCPService):
    async def process_order(self, order_data):
        # Validate
        self.validate(order_data)
        # Process
        result = await self.execute_business_logic(order_data)
        # Return
        return result
```

## Service Architecture

```
┌─────────────────────────────────────┐
│    Client Application               │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────────┐
        │ MCP Service     │
        ├──────────────────┤
        │ • Configuration │
        │ • Error Handler │
        │ • Logger        │
        │ • Health Check  │
        └──────┬──────────┘
               │
        ┌──────▼──────────────────────┐
        │ Domain Implementation       │
        │ • Business Logic            │
        │ • API Integration           │
        │ • Database Access           │
        └──────┬───────────────────────┘
               │
        ┌──────┴───────────────────────┐
        │                              │
    ┌───▼──────┐            ┌────▼────┐
    │ External  │            │Database │
    │ APIs      │            │         │
    └───────────┘            └─────────┘
```

## Service Registration

### Local Service Registry
```python
from mcp_services import ServiceRegistry

registry = ServiceRegistry()

# Register services
registry.register("weather", WeatherService(config))
registry.register("database", DatabaseService(config))
registry.register("auth", AuthService(config))
```

### Service Discovery
```python
# Discover services
services = registry.list_services()

# Get specific service
weather_service = registry.get("weather")

# Check service health
is_healthy = registry.health_check("weather")
```

## Configuration Management

### Service Config
```python
# config.yaml
services:
  weather:
    type: api
    base_url: https://api.weather.com
    api_key: ${WEATHER_API_KEY}
    timeout: 30
    
  database:
    type: postgres
    host: localhost
    port: 5432
    database: mydb
    username: ${DB_USER}
    password: ${DB_PASSWORD}
```

### Environment-Based Configuration
```python
from mcp_services import Config

config = Config.from_env({
    "WEATHER_API_KEY": "api_key",
    "DB_HOST": "localhost",
    "DB_PORT": "5432"
})

service = WeatherService(config)
```

## Error Handling

### Service Errors
```python
from mcp_services import ServiceError, ToolCallError

class ConfigError(ServiceError):
    """Raised when configuration is invalid"""
    pass

class ToolNotFound(ServiceError):
    """Raised when tool doesn't exist"""
    pass

class ToolExecutionError(ToolCallError):
    """Raised when tool execution fails"""
    pass
```

### Error Recovery
```python
class ResilientService(MCPService):
    async def call_tool_with_fallback(self, tool_name, args):
        try:
            return await self.call_tool(tool_name, args)
        except ServiceError as e:
            self.log_error(e)
            return await self.fallback_implementation(tool_name, args)
```

## Logging & Monitoring

### Service Logging
```python
import logging

logger = logging.getLogger("mcp_services")

class MonitoredService(MCPService):
    async def call_tool(self, tool_name, args):
        logger.info(f"Calling {tool_name}")
        start_time = time.time()
        
        try:
            result = await super().call_tool(tool_name, args)
            duration = time.time() - start_time
            logger.info(f"Tool {tool_name} completed in {duration}s")
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {e}")
            raise
```

### Metrics Collection
```python
from prometheus_client import Counter, Histogram

class MetricsService(MCPService):
    def __init__(self, config):
        super().__init__(config)
        self.call_counter = Counter('service_calls', 'Number of service calls')
        self.call_duration = Histogram('service_call_duration', 'Service call duration')
    
    async def call_tool(self, tool_name, args):
        self.call_counter.inc()
        with self.call_duration.time():
            return await super().call_tool(tool_name, args)
```

## Health Checks

### Service Health
```python
class HealthCheckService(MCPService):
    async def health_check(self):
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "uptime": self.get_uptime(),
            "dependencies": await self.check_dependencies()
        }
    
    async def check_dependencies(self):
        checks = {
            "database": await self.check_db(),
            "api": await self.check_api(),
            "cache": await self.check_cache()
        }
        return checks
```

### Liveness & Readiness
```python
async def liveness_probe():
    """Service is alive"""
    return service.is_running()

async def readiness_probe():
    """Service is ready to receive requests"""
    health = await service.health_check()
    return health["status"] == "healthy"
```

## Performance Optimization

### Caching Strategy
```python
from functools import lru_cache

class CachedService(MCPService):
    @lru_cache(maxsize=100)
    async def get_entity(self, entity_id):
        return await self.database.fetch(entity_id)
    
    async def invalidate_cache(self):
        self.get_entity.cache_clear()
```

### Connection Pooling
```python
class PooledService(MCPService):
    def __init__(self, config):
        super().__init__(config)
        self.connection_pool = ConnectionPool(
            min_size=5,
            max_size=20,
            **config["pool"]
        )
```

### Rate Limiting
```python
from ratelimit import limits, sleep_and_retry

class RateLimitedService(MCPService):
    @sleep_and_retry
    @limits(calls=100, period=60)
    async def call_tool(self, tool_name, args):
        return await super().call_tool(tool_name, args)
```

## Testing Services

### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def weather_service():
    config = {"api_key": "test_key"}
    return WeatherService(config)

@pytest.mark.asyncio
async def test_get_weather(weather_service):
    with patch.object(weather_service, 'api_client') as mock:
        mock.get.return_value = {"temperature": 72}
        result = await weather_service.get_weather("NYC")
        assert result["temperature"] == 72
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_service_with_real_api():
    service = WeatherService(real_config)
    result = await service.get_weather("NYC")
    assert "temperature" in result
```

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY services/ ./services/
COPY config/ ./config/

ENV PYTHONUNBUFFERED=1
ENV CONFIG_PATH=/app/config/config.yaml

CMD ["python", "-m", "mcp_services.server"]
```

### Kubernetes Integration
```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-services
spec:
  selector:
    app: mcp-services
  ports:
  - port: 8000
    targetPort: 8000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-services
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-services
  template:
    metadata:
      labels:
        app: mcp-services
    spec:
      containers:
      - name: mcp-services
        image: mcp-services:latest
        ports:
        - containerPort: 8000
```

## Files & Structure
- `mcp_server.py` - Core service implementation
- Additional service implementations

## Dependencies
- fastmcp
- mcp
- httpx
- pydantic
- prometheus-client (optional, for metrics)

## Best Practices
1. Use dependency injection
2. Implement proper error handling
3. Add comprehensive logging
4. Monitor service health
5. Implement caching strategically
6. Use connection pooling
7. Write tests for all services
8. Document service APIs
9. Use configuration management
10. Implement circuit breakers

## Troubleshooting

### Service Not Starting
```python
# Check configuration
config = Config.from_file("config.yaml")
service = WeatherService(config)
service.startup()  # Will raise if config invalid
```

### Tool Not Found
```python
# List available tools
tools = service.list_tools()
print(f"Available tools: {[t.name for t in tools]}")
```

### Performance Issues
```python
# Check service metrics
metrics = service.get_metrics()
print(f"Average call time: {metrics['avg_call_time']}ms")
```

## Future Enhancements
- [ ] Service mesh integration
- [ ] Advanced caching strategies
- [ ] Event streaming
- [ ] Distributed tracing
- [ ] Advanced monitoring
- [ ] Service federation
- [ ] GraphQL API support
