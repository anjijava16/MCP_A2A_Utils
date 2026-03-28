# Fetch MCP Server 🌐

## Overview
An MCP server for fetching and retrieving content from web URLs. Provides tools for HTTP requests, content extraction, and web scraping through MCP interface.

## Features
- **HTTP Requests**: GET, POST, PUT, DELETE methods
- **Content Fetching**: Retrieve webpage content
- **HTML Parsing**: Extract structured data
- **Links Extraction**: Find all links on a page
- **Metadata Extraction**: Get page metadata
- **Error Handling**: Robust error recovery

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp httpx beautifulsoup4 lxml
```

### Configuration
```bash
export FETCH_TIMEOUT=30
export MAX_CONTENT_SIZE=10000000
```

### Running
```bash
python fetch_mcp_server.py
```

## Tools Available

### Basic Fetch
- `fetch_url(url)` - Fetch webpage content
- `fetch_json(url)` - Fetch JSON data
- `fetch_text(url)` - Fetch plain text
- `fetch_html(url)` - Fetch and parse HTML

### HTTP Methods
- `http_get(url, headers)` - HTTP GET request
- `http_post(url, data, headers)` - HTTP POST request
- `http_put(url, data, headers)` - HTTP PUT request
- `http_delete(url, headers)` - HTTP DELETE request

### Content Extraction
- `extract_links(url)` - Extract all links
- `extract_text(url)` - Extract text content
- `extract_table(url, table_index)` - Extract table data
- `extract_metadata(url)` - Get page metadata

### Headers & Configuration
- `set_user_agent(agent)` - Set user agent
- `add_header(name, value)` - Add custom header
- `set_timeout(seconds)` - Set request timeout

## Examples

### Fetching Content
```python
# Fetch webpage
content = fetch_url("https://example.com")
print(content.text)
print(content.status_code)

# Fetch JSON
data = fetch_json("https://api.example.com/data")
print(data)

# Fetch with headers
content = http_get(
    url="https://example.com",
    headers={
        "User-Agent": "Mozilla/5.0",
        "Authorization": "Bearer token"
    }
)
```

### Extracting Data
```python
# Extract all links
links = extract_links("https://example.com")
for link in links:
    print(f"URL: {link['url']}")
    print(f"Text: {link['text']}")

# Extract text
text = extract_text("https://example.com")
print(text)

# Extract table
table = extract_table("https://example.com/data", table_index=0)
for row in table:
    print(row)

# Extract metadata
metadata = extract_metadata("https://example.com")
print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"Author: {metadata['author']}")
```

### API Requests
```python
# POST request
response = http_post(
    url="https://api.example.com/submit",
    data={
        "name": "John",
        "email": "john@example.com"
    },
    headers={"Content-Type": "application/json"}
)

# PUT request
response = http_put(
    url="https://api.example.com/users/123",
    data={"status": "active"}
)

# DELETE request
response = http_delete(
    url="https://api.example.com/users/123"
)
```

## HTML Parsing

### Using BeautifulSoup
```python
# Parse HTML
soup = BeautifulSoup(content, 'html.parser')

# Find elements
title = soup.find('h1').text

# Find all elements
paragraphs = soup.find_all('p')

# CSS selectors
items = soup.select('.item')

# Attributes
links = soup.find_all('a', class_='external')
```

## Error Handling

### Connection Errors
```python
try:
    content = fetch_url("https://nonexistent.example.com")
except ConnectionError:
    print("Connection failed")
except TimeoutError:
    print("Request timeout")
```

### Status Codes
```python
response = http_get("https://example.com")

if response.status_code == 200:
    print("Success")
elif response.status_code == 404:
    print("Not found")
elif response.status_code == 500:
    print("Server error")
```

## Performance Optimization

### Caching
```python
# Cache responses
cache = {}

def fetch_cached(url):
    if url in cache:
        return cache[url]
    
    content = fetch_url(url)
    cache[url] = content
    return content
```

### Connection Pooling
```python
# Reuse connections
session = httpx.Client(
    limits=httpx.Limits(max_keepalive_connections=5)
)
```

## Testing

### Unit Tests
```python
def test_fetch_url():
    content = fetch_url("https://example.com")
    assert content.status_code == 200

def test_extract_links():
    links = extract_links("https://example.com")
    assert len(links) > 0
```

## Configuration

### Request Config
```python
FETCH_CONFIG = {
    "timeout": 30,
    "max_size": 10_000_000,
    "verify_ssl": True,
    "follow_redirects": True,
    "max_redirects": 5
}
```

### Headers Config
```python
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Encoding": "gzip, deflate"
}
```

## Use Cases
- Web scraping
- Content aggregation
- API testing
- Data extraction
- Link validation
- Metadata extraction
- Feed parsing

## Best Practices
1. Respect robots.txt
2. Set appropriate timeouts
3. Handle redirects
4. Add user agent
5. Implement rate limiting
6. Use caching
7. Handle errors gracefully
8. Log requests

## Troubleshooting

### SSL Errors
```python
# Disable SSL verification (not recommended)
response = http_get(url, verify_ssl=False)
```

### Timeout Issues
```python
# Increase timeout
set_timeout(60)  # 60 seconds
```

### Character Encoding
```python
# Handle encoding
content = fetch_url(url)
content.encoding = 'utf-8'
```

## Future Enhancements
- [ ] JavaScript rendering
- [ ] Proxy support
- [ ] Cookie handling
- [ ] Session management
- [ ] Form submission
