# Server Filesystem MCP 📂

## Overview
A reference implementation of a filesystem MCP server based on the official Model Context Protocol specification. This server demonstrates best practices for file system operations with proper error handling, security, and performance optimization.

## Features
- **Reference Implementation**: Based on official MCP spec
- **Safe File Operations**: Sandboxed filesystem access
- **Comprehensive Tools**: Read, write, list, manage files
- **Error Handling**: Graceful error recovery
- **Performance**: Optimized file operations
- **Cross-Platform**: Works on Linux, macOS, Windows

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp
```

### Configuration
Set sandbox root:
```bash
export MCP_SANDBOX_ROOT="/tmp/mcp_sandbox"
```

### Running
```bash
python server-filesystem-mcp.py
```

## Tools Available

### File Operations
- `read_file(path)` - Read file contents
- `write_file(path, content)` - Write to file
- `create_file(path, content)` - Create new file
- `delete_file(path)` - Delete file
- `file_exists(path)` - Check existence
- `get_file_size(path)` - Get file size

### Directory Operations
- `list_directory(path)` - List contents
- `create_directory(path)` - Create directory
- `delete_directory(path)` - Delete directory
- `get_directory_tree(path)` - Get full tree

### File Metadata
- `get_file_info(path)` - Get file metadata
- `get_file_permissions(path)` - Get permissions
- `set_file_permissions(path, mode)` - Change permissions
- `get_modified_time(path)` - Get modification time

### Path Operations
- `get_absolute_path(path)` - Resolve to absolute
- `normalize_path(path)` - Normalize path
- `get_relative_path(base, target)` - Get relative path

## Security Model

### Sandbox Enforcement
```python
# All operations confined to sandbox root
SANDBOX_ROOT = "/tmp/mcp_sandbox"

# Path validation
def check_path(user_path):
    real_path = os.path.realpath(user_path)
    if not real_path.startswith(SANDBOX_ROOT):
        raise PermissionError("Access denied")
    return real_path
```

### Restrictions
- No symlink escape
- No parent directory traversal
- Path must be within sandbox
- Permission checking

## File Operations

### Read File
```python
content = read_file("document.txt")
# Returns: file contents as string
```

### Write File
```python
write_file(
    "output.txt",
    "New content",
    encoding="utf-8"
)
# Creates or overwrites
```

### Directory Listing
```python
files = list_directory("./")
# Returns: [...{name, type, size}]
```

## Use Cases
- Document management
- Log file processing
- Configuration management
- Data analysis on files
- File transformation
- Backup operations

## Error Handling

### Path Validation
```python
try:
    content = read_file("/etc/passwd")
except PermissionError:
    print("Path outside sandbox")
except FileNotFoundError:
    print("File not found")
```

### Large Files
```python
# Handle large files efficiently
with open(path, 'r', buffering=8192) as f:
    for chunk in iter(lambda: f.read(8192), ''):
        process(chunk)
```

## Performance Optimization
- Efficient I/O operations
- Streaming for large files
- Directory caching
- Lazy loading

## Configuration

### Sandbox Root
```bash
export MCP_SANDBOX_ROOT="/data/mcp"
```

### Max File Size
```python
MAX_FILE_SIZE = 100_000_000  # 100MB
```

## Testing

### Unit Tests
```python
@pytest.mark.asyncio
async def test_read_file():
    content = read_file("test.txt")
    assert len(content) > 0
```

## Dependencies
- fastmcp
- mcp

## Best Practices
1. Always validate paths
2. Use absolute paths
3. Handle encoding properly
4. Close files after use
5. Check file existence
6. Use appropriate permissions
7. Log operations

## Troubleshooting

### Path Issues
- Verify path is within sandbox
- Check for symlinks
- Use forward slashes

### Permission Errors
- Verify file permissions
- Check sandbox root
- Review path validation

## Future Enhancements
- [ ] Symlink support
- [ ] Directory watching
- [ ] Compression tools
- [ ] File search
- [ ] Backup utilities
