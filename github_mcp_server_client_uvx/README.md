# GitHub MCP Server Client 🐙

## Overview
A comprehensive MCP client for GitHub API integration, enabling access to repositories, issues, pull requests, and workflows through MCP tools. Integrates with GitHub's REST and GraphQL APIs.

## Features
- **Repository Management**: Access and manage repos
- **Issue Tracking**: Create, update, manage issues
- **Pull Requests**: Manage PR workflows
- **Code Search**: Search code and repos
- **Actions Integration**: Interact with GitHub Actions
- **User & Org Management**: User and organization tools

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp httpx PyGithub
```

### Configuration
```bash
export GITHUB_TOKEN="ghp_..."  # Personal access token
export GITHUB_ORG="your-org"   # Organization name
```

### Running
```python
from github_mcp_client import GitHubMCPClient

client = GitHubMCPClient(token=os.getenv("GITHUB_TOKEN"))
repos = client.list_repositories()
```

## Tools Available

### Repository Operations
- `list_repositories(org)` - List org repositories
- `get_repository(owner, repo)` - Get repo details
- `create_repository(name, description)` - Create repo
- `get_repo_stats(owner, repo)` - Get repo statistics
- `search_repositories(query)` - Search repos

### Issue Management
- `list_issues(owner, repo)` - List issues
- `get_issue(owner, repo, number)` - Get issue details
- `create_issue(owner, repo, title, body)` - Create issue
- `update_issue(owner, repo, number, state)` - Update issue
- `add_issue_label(owner, repo, number, label)` - Add label
- `comment_on_issue(owner, repo, number, comment)` - Comment

### Pull Request Management
- `list_pull_requests(owner, repo)` - List PRs
- `get_pull_request(owner, repo, number)` - Get PR details
- `create_pull_request(owner, repo, title, body)` - Create PR
- `approve_pull_request(owner, repo, number)` - Approve PR
- `merge_pull_request(owner, repo, number)` - Merge PR
- `request_review(owner, repo, number, reviewer)` - Request review

### Code Operations
- `search_code(query)` - Search repositories
- `get_file(owner, repo, path)` - Get file raw content
- `get_blob(owner, repo, sha)` - Get blob
- `list_commits(owner, repo)` - List commits
- `get_commit(owner, repo, sha)` - Get commit details

### GitHub Actions
- `list_workflows(owner, repo)` - List workflows
- `trigger_workflow(owner, repo, workflow_id)` - Trigger workflow
- `get_workflow_runs(owner, repo, workflow_id)` - Get workflow runs
- `get_workflow_run_details(owner, repo, run_id)` - Get run details

### User & Organization
- `get_user_info(username)` - Get user details
- `get_org_info(org)` - Get organization details
- `list_org_members(org)` - List org members
- `get_user_repos(username)` - List user repositories

## Examples

### Repository Management
```python
# List repositories
repos = client.list_repositories("pytorch")
for repo in repos:
    print(f"{repo['name']}: {repo['description']}")

# Get repository details
repo = client.get_repository("pytorch", "pytorch")
print(f"Stars: {repo['stargazers_count']}")
print(f"Forks: {repo['forks_count']}")
print(f"Language: {repo['language']}")
```

### Issue Management
```python
# List open issues
issues = client.list_issues("owner", "repo")
for issue in issues:
    print(f"#{issue['number']}: {issue['title']}")

# Create issue
new_issue = client.create_issue(
    owner="owner",
    repo="repo",
    title="Bug: Something broken",
    body="Description of the bug..."
)

# Add label to issue
client.add_issue_label(
    owner="owner",
    repo="repo",
    number=42,
    label="bug"
)
```

### Pull Request Workflow
```python
# List pull requests
prs = client.list_pull_requests("owner", "repo")

# Create pull request
pr = client.create_pull_request(
    owner="owner",
    repo="repo",
    title="Feature: Add new functionality",
    body="Description of changes...",
    head="feature-branch",
    base="main"
)

# Request review
client.request_review(
    owner="owner",
    repo="repo",
    number=pr['number'],
    reviewer="reviewer-username"
)

# Merge PR when ready
client.merge_pull_request(
    owner="owner",
    repo="repo",
    number=pr['number']
)
```

### Code Search
```python
# Search code
results = client.search_code("def neural_network")

# Get specific file
content = client.get_file(
    owner="owner",
    repo="repo",
    path="src/model.py"
)

# Get commit details
commit = client.get_commit(
    owner="owner",
    repo="repo",
    sha="abc123"
)
```

### GitHub Actions
```python
# List workflows
workflows = client.list_workflows("owner", "repo")

# Trigger workflow
client.trigger_workflow(
    owner="owner",
    repo="repo",
    workflow_id="tests.yml"
)

# Check workflow runs
runs = client.get_workflow_runs(
    owner="owner",
    repo="repo",
    workflow_id="tests.yml"
)

# Get run details
details = client.get_workflow_run_details(
    owner="owner",
    repo="repo",
    run_id="123456"
)
```

## Authentication

### Personal Access Token
```bash
# Generate at https://github.com/settings/tokens
export GITHUB_TOKEN="ghp_..."

# Usage
client = GitHubMCPClient(token=os.getenv("GITHUB_TOKEN"))
```

### Permissions
Required token scopes:
- `repo` - Repository access
- `workflow` - Actions workflows
- `admin:org` - Organization administration (optional)

## Rate Limiting

### API Rate Limits
```python
# GitHub API has rate limits
# - Authenticated: 5000 requests/hour
# - Unauthenticated: 60 requests/hour

# Check rate limit
rate_limit = client.get_rate_limit()
print(f"Remaining: {rate_limit['core']['remaining']}")
```

### Handling Rate Limits
```python
# Exponential backoff
import time

def call_with_backoff(func, *args, **kwargs):
    retries = 0
    while retries < 3:
        try:
            return func(*args, **kwargs)
        except GitHubException as e:
            if e.status == 403:  # Rate limited
                wait_time = 2 ** retries
                time.sleep(wait_time)
                retries += 1
            else:
                raise
```

## Use Cases
- Automated issue management
- PR automation and review
- Repository monitoring
- Code search and analysis
- CI/CD integration
- Project metrics collection
- Workflow automation

## Advanced Features

### Batch Operations
```python
# Process multiple repos
for repo in client.list_repositories("org"):
    stats = client.get_repo_stats(repo['owner']['login'], repo['name'])
    # Process stats
```

### Custom Queries
```python
# GraphQL support for complex queries
query = """
query {
    repository(owner: "owner", name: "repo") {
        issues(first: 10, states: OPEN) {
            totalCount
            edges {
                node {
                    number
                    title
                }
            }
        }
    }
}
"""

result = client.execute_graphql(query)
```

## Configuration

### Client Config
```python
GITHUB_CONFIG = {
    "base_url": "https://api.github.com",
    "per_page": 30,
    "timeout": 30,
    "retry_attempts": 3
}
```

## Testing

### Unit Tests
```python
@pytest.mark.asyncio
async def test_list_repos():
    client = GitHubMCPClient(token="test_token")
    repos = client.list_repositories("torvalds")
    assert len(repos) > 0

def test_issue_creation():
    issue = client.create_issue(
        owner="test",
        repo="test",
        title="Test issue"
    )
    assert issue['number'] > 0
```

## Dependencies
- fastmcp
- mcp
- httpx
- PyGithub

## Best Practices
1. Use personal access tokens, not passwords
2. Rotate tokens regularly
3. Limit token scope to needed permissions
4. Handle rate limits gracefully
5. Use batch operations
6. Monitor API usage
7. Implement retry logic
8. Cache results when possible

## Troubleshooting

### Authentication Errors
```python
# Verify token is valid
try:
    user = client.get_user_info(username)
except AuthenticationError:
    print("Invalid token or permissions")
```

### Rate Limit Issues
```python
# Check current limits
limit = client.get_rate_limit()
if limit['core']['remaining'] < 100:
    print("Approaching rate limit")
```

## Future Enhancements
- [ ] Advanced search filters
- [ ] Webhook management
- [ ] Gist management
- [ ] Repository templates
- [ ] Discussion support
- [ ] Projects (beta) support
- [ ] Codespaces integration
