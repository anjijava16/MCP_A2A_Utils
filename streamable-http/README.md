# Streamable HTTP MCP 🌊

## Overview
A specialized MCP server for streaming large data transfers and real-time data flows via HTTP. This server supports chunked responses, Server-Sent Events (SSE), and WebSocket connections for efficient streaming of data.

## Features
- **HTTP Streaming**: Efficient large data transfer
- **Server-Sent Events**: Real-time data streaming
- **WebSocket Support**: Bidirectional streaming
- **Chunked Responses**: Flexible response sizes
- **Backpressure Handling**: Flow control
- **Error Recovery**: Graceful error handling

## Architecture

```
Client
    ↓ (HTTP/WebSocket)
Streamable HTTP Server
    ├── Stream Manager
    ├── Chunk Handler
    ├── SSE Handler
    └── WebSocket Manager
```

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp httpx websockets
```

### Configuration
```bash
export STREAM_PORT=8000
export CHUNK_SIZE=8192
export STREAM_TIMEOUT=300
```

### Running
```bash
python streamable_http_server.py
```

## Tools Available

### Stream Operations
- `create_stream(name, source)` - Create new stream
- `read_stream_chunk(stream_id, size)` - Read chunk
- `close_stream(stream_id)` - Close stream
- `get_stream_status(stream_id)` - Stream status

### SSE Operations
- `subscribe_to_stream(stream_id)` - Subscribe to SSE
- `unsubscribe_from_stream(stream_id)` - Unsubscribe
- `broadcast_event(event, data)` - Broadcast to subscribers

### WebSocket Operations
- `connect_websocket(url)` - Connect WebSocket
- `send_message(ws_id, message)` - Send on WebSocket
- `receive_message(ws_id)` - Receive from WebSocket

## Stream Types

### File Streaming
```python
# Stream large files
stream = create_stream(
    name="large_file.zip",
    source="file:///path/to/file.zip"
)

# Read in chunks
while not stream.is_complete():
    chunk = read_stream_chunk(stream.id, chunk_size=8192)
    process(chunk)
```

### Data Streaming
```python
# Stream database results
stream = create_stream(
    name="query_results",
    source="database://query_id"
)

# Continuous reading
for chunk in stream.iter_chunks():
    handle_data(chunk)
```

### Event Streaming
```python
# Stream events with SSE
subscribe_to_stream("events")

# Receive events
for event in stream.iter_events():
    process_event(event)
```

## HTTP Streaming Examples

### Chunked Transfer
```python
@app.get("/stream/{stream_id}")
async def stream_data(stream_id: str):
    stream = get_stream(stream_id)
    
    async def generate():
        while not stream.is_complete():
            chunk = stream.read_chunk(size=8192)
            yield chunk
    
    return StreamingResponse(
        generate(),
        media_type="application/octet-stream"
    )
```

### Server-Sent Events
```python
@app.get("/sse/{stream_id}")
async def stream_sse(stream_id: str):
    stream = get_stream(stream_id)
    
    async def event_generator():
        while True:
            data = await stream.next_event()
            yield f"data: {json.dumps(data)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

### WebSocket Streaming
```python
@app.websocket("/ws/{stream_id}")
async def websocket_stream(websocket, stream_id: str):
    await websocket.accept()
    stream = get_stream(stream_id)
    
    while True:
        chunk = await stream.next_chunk()
        await websocket.send_bytes(chunk)
```

## Performance Optimization

### Chunk Size Optimization
```python
# Adaptive chunk sizing
chunk_size = calculate_optimal_size(
    bandwidth=current_bandwidth,
    latency=current_latency
)
```

### Buffering
```python
# Use buffer for smooth streaming
buffer = StreamBuffer(
    max_size=100,
    low_watermark=20,
    high_watermark=80
)
```

### Compression
```python
# Optional compression
stream = create_stream(
    source=source,
    compression="gzip",
    compression_level=6
)
```

## Error Handling

### Connection Recovery
```python
async def stream_with_recovery(stream_id):
    stream = get_stream(stream_id)
    
    while not stream.is_complete():
        try:
            chunk = await stream.next_chunk(timeout=30)
            yield chunk
        except ConnectionError:
            # Reconnect and resume
            stream = stream.resume()
```

### Timeout Handling
```python
# Handle slow clients
try:
    chunk = await stream.next_chunk(timeout=60)
except TimeoutError:
    stream.pause()
    # Wait for client recovery
```

## Use Cases
- Large file transfers
- Real-time data feeds
- Video streaming
- Log streaming
- Database result streaming
- IoT data collection
- Live dashboards

## Backpressure Management

### Flow Control
```python
class StreamBuffer:
    def write(self, data):
        if len(self.buffer) > self.high_watermark:
            # Pause upstream
            self.pause_upstream()
        
        self.buffer.append(data)
    
    def read(self, size):
        chunk = self.buffer[:size]
        
        if len(self.buffer) < self.low_watermark:
            # Resume upstream
            self.resume_upstream()
        
        return chunk
```

## Monitoring

### Stream Metrics
- Throughput (bytes/second)
- Chunk latency
- Active streams
- Buffer usage
- Error rate

### Performance Tracking
```python
metrics = {
    "throughput": stream.bytes_sent / elapsed_time,
    "chunk_latency": avg_chunk_time,
    "active_streams": num_active,
    "buffer_usage": buffer.size / buffer.max_size
}
```

## Testing

### Load Testing
```python
# Test with large data
large_file = generate_test_file(size="1GB")
stream = create_stream(source=large_file)

# Measure throughput
start = time.time()
total_bytes = 0
while not stream.is_complete():
    chunk = stream.read_chunk(8192)
    total_bytes += len(chunk)

throughput = total_bytes / (time.time() - start)
print(f"Throughput: {throughput / 1024 / 1024:.2f} MB/s")
```

## Configuration Options

### Server Config
```python
STREAM_CONFIG = {
    "chunk_size": 8192,
    "buffer_size": 100,
    "stream_timeout": 300,
    "max_concurrent_streams": 100,
    "compression": "gzip",
    "compression_level": 6
}
```

## Dependencies
- fastmcp
- mcp
- httpx
- websockets
- aiofiles (for async file operations)

## Best Practices
1. Set appropriate chunk sizes
2. Implement proper backpressure handling
3. Add request/response validation
4. Monitor stream health
5. Handle disconnections gracefully
6. Compress when beneficial
7. Set reasonable timeouts
8. Clean up resources

## Troubleshooting

### Slow Throughput
- Check chunk size
- Monitor network conditions
- Review compression settings
- Check buffer configuration

### Connection Drops
- Implement reconnection logic
- Add heartbeat monitoring
- Handle timeouts properly
- Use connection pooling

## Future Enhancements
- [ ] Adaptive bitrate streaming
- [ ] End-to-end encryption
- [ ] Multipart chunking
- [ ] Resume capability
- [ ] Peer-to-peer streaming
