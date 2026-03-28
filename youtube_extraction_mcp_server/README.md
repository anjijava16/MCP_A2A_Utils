# MCP YouTube Transcript Extractor 📹

## Overview
A FastMCP-based server that extracts transcripts from YouTube videos. This server integrates with the YouTube Transcript API to provide full video transcripts in text format, enabling content analysis and summarization of video content.

## Features
- **Transcript Extraction**: Get full transcripts from YouTube videos
- **URL Parsing**: Automatically parses various YouTube URL formats
- **Timestamp Preservation**: Maintains timing information (optional)
- **Error Handling**: Graceful handling for unavailable transcripts
- **Language Support**: Works with videos in multiple languages

## Tools Available
- `get_youtube_transcript(url)` - Extract transcript from YouTube video
  - Input: YouTube URL (various formats supported)
  - Output: Full transcript text or error message

## Setup & Usage

### Installation
```bash
pip install fastmcp youtube-transcript-api
```

### Running the Server
```bash
# Stdio transport (for Claude Desktop)
python yt_transcript.py

# SSE transport (for HTTP clients)
# Default port may vary
```

### Supported URL Formats
The server supports various YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`
- Short links and embedded URL variations

### Example Usage
```python
# Extract transcript from YouTube video
transcript = get_youtube_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Returns:
{
    "transcript": "Full transcript text here...",
    "length": 3250,  # characters
    "status": "success"
}

# Or if unavailable:
{
    "error": "Transcript not available for this video"
}
```

## Transcript Format
The extracted transcript contains:
- Complete video script/dialogue
- Formatted text with proper spacing
- Readable format suitable for analysis
- Can be processed for summarization

## Files
- `yt_transcript.py` - Main YouTube transcript extractor

## Use Cases
- **Content Analysis**: Analyze video content without watching
- **Summarization**: Create summaries of video content
- **Research**: Extract information from educational videos
- **Accessibility**: Provide text representation of video content
- **SEO Optimization**: Generate content from video transcripts

## Limitations
- Only works with videos that have transcripts available
- May not work with community-generated subtitles in some cases
- Depends on YouTube's availability
- Handles official transcripts and auto-generated captions

## Error Handling
- Invalid URL detection and messaging
- Missing transcript handling
- API availability checks
- Proper error response formatting

## Dependencies
- fastmcp
- youtube-transcript-api
- mcp

## Performance
- Fast transcript retrieval
- Minimal processing overhead
- Efficient URL parsing

## Future Enhancements
- Support for multiple languages and auto-translation
- Timestamp-based segment extraction
- Speaker identification (if available)
- Keyword extraction from transcripts
