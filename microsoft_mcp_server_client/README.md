# Microsoft MCP Server Client 🔷

## Overview
A specialized MCP client for Microsoft services integration, enabling access to Microsoft 365, Azure services, and Microsoft Graph API through MCP tools. Provides seamless integration with Microsoft's cloud ecosystem.

## Features
- **Microsoft Graph API**: Access enterprise data
- **Office 365 Integration**: Email, calendar, documents
- **Teams Integration**: Chat and collaboration
- **Azure Services**: Compute, storage, databases
- **SharePoint**: Document management
- **OneDrive**: Cloud storage operations

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp azure-identity msgraph-core
```

### Configuration
```bash
export MICROSOFT_APP_ID="your_app_id"
export MICROSOFT_TENANT_ID="your_tenant_id"
export MICROSOFT_CLIENT_SECRET="your_secret"
```

### Running
```python
from microsoft_mcp_client import MicrosoftMCPClient

client = MicrosoftMCPClient(
    app_id=os.getenv("MICROSOFT_APP_ID"),
    tenant_id=os.getenv("MICROSOFT_TENANT_ID"),
    client_secret=os.getenv("MICROSOFT_CLIENT_SECRET")
)

# Use Microsoft services
email_list = client.list_emails()
```

## Tools Available

### Email Management
- `list_emails(folder, limit)` - List emails
- `get_email(message_id)` - Get email details
- `send_email(to, subject, body)` - Send email
- `create_draft(to, subject, body)` - Create draft
- `delete_email(message_id)` - Delete email
- `move_email(message_id, folder)` - Move to folder

### Calendar Management
- `list_events(start_date, end_date)` - List events
- `get_event(event_id)` - Get event details
- `create_event(title, start, end, attendees)` - Create event
- `update_event(event_id, updates)` - Update event
- `delete_event(event_id)` - Delete event
- `find_meeting_times(attendees, duration)` - Find slots

### Teams Integration
- `list_teams()` - List teams
- `list_channels(team_id)` - List team channels
- `send_message(channel_id, message)` - Send message
- `get_messages(channel_id)` - Get channel messages
- `create_team(name, description)` - Create team
- `get_team_members(team_id)` - List team members

### SharePoint & OneDrive
- `list_files(folder_path)` - List files
- `upload_file(path, file_content)` - Upload file
- `download_file(file_id)` - Download file
- `delete_file(file_id)` - Delete file
- `share_file(file_id, user_email)` - Share with user
- `get_file_properties(file_id)` - Get file metadata

### User & Organization
- `get_user_info()` - Get current user
- `get_user_profile(user_id)` - Get user profile
- `list_users()` - List organization users
- `get_organization_info()` - Get org details
- `search_users(query)` - Search users

## Examples

### Email Operations
```python
# List recent emails
emails = client.list_emails(
    folder="inbox",
    limit=10
)

for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Received: {email['received_datetime']}")

# Send email
client.send_email(
    to="user@example.com",
    subject="Meeting Recap",
    body="Here are the action items from today's meeting..."
)

# Move email to folder
client.move_email(
    message_id="msg_123",
    folder="archive"
)
```

### Calendar Management
```python
# Get calendar events
events = client.list_events(
    start_date="2024-06-01",
    end_date="2024-06-30"
)

for event in events:
    print(f"{event['subject']}: {event['start']} - {event['end']}")

# Create meeting
event = client.create_event(
    title="Team Standup",
    start="2024-06-20 10:00:00",
    end="2024-06-20 10:30:00",
    attendees=["alice@company.com", "bob@company.com"]
)

# Find available meeting times
slots = client.find_meeting_times(
    attendees=["alice@company.com", "bob@company.com"],
    duration=30  # minutes
)

for slot in slots:
    print(f"Available: {slot['start']} - {slot['end']}")
```

### Teams Integration
```python
# List teams
teams = client.list_teams()

for team in teams:
    print(f"Team: {team['display_name']}")
    
    # List channels in team
    channels = client.list_channels(team['id'])
    for channel in channels:
        print(f"  Channel: {channel['display_name']}")

# Send message to channel
client.send_message(
    channel_id="chan_123",
    message="@channel This is important!"
)

# Get recent messages
messages = client.get_messages(channel_id="chan_123")

for msg in messages:
    print(f"{msg['from']}: {msg['body']}")
```

### File Operations
```python
# List OneDrive files
files = client.list_files("/documents")

for file in files:
    print(f"{file['name']}: {file['size']} bytes")

# Upload file
with open("report.pdf", "rb") as f:
    client.upload_file(
        path="/documents/reports/report.pdf",
        file_content=f.read()
    )

# Share file
client.share_file(
    file_id="file_123",
    user_email="colleague@company.com"
)
```

## Authentication

### Azure OAuth 2.0
```bash
# Register application in Azure AD
# Get: App ID, Tenant ID, Client Secret

# Use client credentials flow
client = MicrosoftMCPClient(
    app_id="your_app_id",
    tenant_id="your_tenant_id",
    client_secret="your_secret"
)
```

### Permissions Required
```
Mail.Read, Mail.Send
Calendar.Read, Calendar.ReadWrite
Team.ReadBasic.All, TeamSettings.ReadWrite.All
Files.ReadWrite
User.Read, User.ReadBasic.All
```

## Batch Operations

### Batch Email Operations
```python
# Process multiple emails
email_ids = ["msg_1", "msg_2", "msg_3"]

for email_id in email_ids:
    email = client.get_email(email_id)
    # Process email
    if should_archive(email):
        client.move_email(email_id, "archive")
```

### Batch File Operations
```python
# Upload multiple files
for file_path in file_list:
    with open(file_path, "rb") as f:
        client.upload_file(
            path=f"/backup/{os.path.basename(file_path)}",
            file_content=f.read()
        )
```

## Advanced Features

### Search
```python
# Search emails
results = client.search_emails(
    query="from:boss@company.com subject:urgent",
    limit=20
)

# Search files
files = client.search_files(
    query="*.xlsx modified:last_week",
    limit=50
)
```

### Graph API Queries
```python
# Direct Graph API queries for advanced use cases
query = """
/me/messages?$filter=from/emailAddress/address eq 'user@example.com'
&$orderby=receivedDateTime desc
&$select=subject,from,receivedDateTime
"""

results = client.execute_graph_query(query)
```

## Use Cases
- Email automation
- Calendar management
- Team collaboration
- Document management
- User administration
- Meeting scheduling
- Workflow automation

## Configuration

### Client Config
```python
MICROSOFT_CONFIG = {
    "graph_api_version": "v1.0",
    "timeout": 30,
    "retry_attempts": 3,
    "batch_size": 20
}
```

## Error Handling

### Authentication Errors
```python
try:
    client = MicrosoftMCPClient(app_id, tenant_id, secret)
except AuthenticationError:
    print("Invalid credentials")
```

### Rate Limiting
```python
try:
    emails = client.list_emails()
except RateLimitError as e:
    wait_time = e.retry_after
    time.sleep(wait_time)
```

## Testing

### Unit Tests
```python
def test_list_emails():
    emails = client.list_emails()
    assert len(emails) > 0
    assert "from" in emails[0]

def test_send_email():
    result = client.send_email(
        to="test@example.com",
        subject="Test",
        body="Test message"
    )
    assert result["success"] == True
```

## Dependencies
- fastmcp
- mcp
- azure-identity
- msgraph-core
- httpx

## Best Practices
1. Use service accounts for automation
2. Implement error handling
3. Cache frequently accessed data
4. Respect rate limits
5. Monitor permission changes
6. Log sensitive operations
7. Implement retry logic
8. Use batch operations

## Troubleshooting

### Connection Issues
Check:
- Credentials validity
- Network connectivity
- Tenant ID correctness
- App registration status

### Permission Errors
- Verify OAuth scopes
- Check app permissions in Azure
- Review admin consent

## Future Enhancements
- [ ] Advanced filtering
- [ ] Webhook subscriptions
- [ ] Automation rules
- [ ] Document intelligence
- [ ] Real-time chat
- [ ] Advanced search
