from mcp.server.fastmcp import FastMCP
from typing import List

import youtube_transcript_api

# In-memory mock database with 20 leave days to start
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}

# Create MCP server
mcp = FastMCP("LeaveManager")


# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."
# @mcp.tool()
# def get_youtube_transcript(url: str) -> dict:
#     """Fetches transcript from a given YouTube URL."""
#     video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
#     if not video_id_match:
#         return {"error": "Invalid YouTube URL"}

#     video_id = video_id_match.group(1)

#     try:
#         transcript = youtube_transcript_api.get_transcript(video_id)
#         transcript_text = "\n".join([entry["text"] for entry in transcript])
#         return {"transcript": transcript_text}
#     except Exception as e:
#         return {"error": str(e)}

from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


@mcp.tool()
def get_youtube_transcript(url: str) -> dict:
    """Fetches transcript from a given YouTube URL."""

    try:
        parsed_url = urlparse(url)
        if "youtube.com" in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
        elif "youtu.be" in parsed_url.netloc:
            video_id = parsed_url.path.lstrip("/")
        else:
            return {"error": "Unsupported YouTube URL format"}

        if not video_id or len(video_id) != 11:
            return {"error": "Invalid YouTube video ID"}

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([entry["text"] for entry in transcript])
        return {"transcript": transcript_text}
    except Exception as e:
        return {"error": str(e)}

# Tool: Apply for Leave with specific dates
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."


# Resource: Leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return "Employee ID not found."


# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"


if __name__ == "__main__":
    mcp.run()
