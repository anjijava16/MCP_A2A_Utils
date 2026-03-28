# Time MCP Server & Client ⏰

## Overview
A specialized MCP server and client for time and timezone operations, scheduling, and temporal data manipulation. Provides comprehensive time management tools for agents and applications.

## Features
- **Timezone Support**: Convert between timezones
- **Scheduling**: Schedule tasks and events
- **Duration Calculations**: Calculate time differences
- **Formatting**: Format times for display
- **Recurring Events**: Handle recurring schedules
- **Calendar Integration**: Calendar operations

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp pytz python-dateutil
```

### Configuration
```bash
export DEFAULT_TIMEZONE="UTC"
export TIMEZONE_DATABASE="olson"
```

### Running
```bash
python time_mcp_server.py
```

## Tools Available

### Time Operations
- `get_current_time(timezone)` - Get current time
- `convert_timezone(time, from_tz, to_tz)` - Convert timezone
- `get_timezone_info(timezone)` - Get timezone details
- `list_timezones()` - List all timezones

### Duration & Calculations
- `calculate_duration(start, end)` - Calculate duration
- `add_duration(time, duration)` - Add duration to time
- `parse_duration(duration_string)` - Parse duration

### Scheduling
- `schedule_event(name, time, timezone)` - Schedule event
- `get_scheduled_events()` - List events
- `reschedule_event(event_id, new_time)` - Reschedule
- `cancel_event(event_id)` - Cancel event

### Calendar
- `get_calendar_day(date)` - Get day information
- `get_calendar_month(year, month)` - Get month calendar
- `is_business_day(date)` - Check if business day
- `get_holidays(year, country)` - Get holidays

## Examples

### Time Zone Conversion
```python
# Get current time in different zones
utc_time = get_current_time("UTC")
ny_time = get_current_time("America/New_York")
tokyo_time = get_current_time("Asia/Tokyo")

# Convert between zones
result = convert_timezone(
    time="2024-06-15 14:30:00",
    from_tz="UTC",
    to_tz="America/Los_Angeles"
)
# Returns: 2024-06-15 07:30:00 PDT
```

### Duration Calculations
```python
# Calculate duration between times
duration = calculate_duration(
    start="2024-06-15 09:00:00",
    end="2024-06-15 17:30:00"
)
# Returns: 8 hours 30 minutes

# Add duration to time
result = add_duration(
    time="2024-06-15 14:00:00",
    duration="2 hours 30 minutes"
)
# Returns: 2024-06-15 16:30:00
```

### Event Scheduling
```python
# Schedule an event
event = schedule_event(
    name="Team Meeting",
    time="2024-06-20 10:00:00",
    timezone="America/New_York"
)

# Get all scheduled events
events = get_scheduled_events()

# Reschedule
reschedule_event(
    event_id=event['id'],
    new_time="2024-06-20 15:00:00"
)

# Cancel
cancel_event(event_id=event['id'])
```

### Calendar Operations
```python
# Get calendar information
day_info = get_calendar_day("2024-06-15")
# Returns: {
#   "date": "2024-06-15",
#   "day_of_week": "Saturday",
#   "week_number": 35,
#   "is_business_day": False
# }

# Check if business day
is_business = is_business_day("2024-06-15")

# Get holidays
holidays = get_holidays(year=2024, country="US")
```

## Timezone Support

### Major Timezones
```python
timezones = list_timezones()
# Common timezones:
# - UTC
# - America/New_York
# - America/Los_Angeles
# - Europe/London
# - Europe/Paris
# - Asia/Tokyo
# - Asia/Shanghai
# - Australia/Sydney
# - ... and 400+ more
```

### Getting Timezone Info
```python
info = get_timezone_info("America/New_York")
# Returns: {
#   "name": "America/New_York",
#   "abbreviation": "EST/EDT",
#   "utc_offset": -5,
#   "dst_active": False,
#   "aliases": ["America/New_York", ...]
# }
```

## Scheduling Use Cases

### Meeting Scheduler
```python
# Find optimal meeting time
def find_meeting_time(participants_timezones):
    """Find 9-5 business hours for all participants"""
    # Get current time in all zones
    times = {}
    for tz in participants_timezones:
        times[tz] = get_current_time(tz)
    
    # Find overlap
    # ... logic to find common 9-5 window
    
    return optimal_time
```

### Reminder System
```python
# Schedule reminders
events = [
    {"name": "Daily standup", "time": "09:00", "tz": "UTC"},
    {"name": "Team sync", "time": "14:00", "tz": "UTC"},
    {"name": "EOD review", "time": "17:00", "tz": "UTC"}
]

for event in events:
    schedule_event(event['name'], event['time'], event['tz'])
```

## Calendar Features

### Business Day Detection
```python
# Check multiple days
dates = ["2024-06-14", "2024-06-15", "2024-06-17"]
for date in dates:
    is_business = is_business_day(date)
    print(f"{date}: {'Yes' if is_business else 'No'}")
```

### Holiday Handling
```python
# Get holidays for planning
holidays = get_holidays(year=2024, country="US")

# Skip holidays in calculations
def add_business_days(start_date, days, holidays):
    current = start_date
    added = 0
    
    while added < days:
        current += timedelta(days=1)
        if is_business_day(current) and current not in holidays:
            added += 1
    
    return current
```

## Advanced Features

### Recurring Events
```python
# Schedule recurring event
event = schedule_event(
    name="Weekly team meeting",
    time="2024-06-20 10:00:00",
    timezone="America/New_York",
    recurrence="weekly",
    recurrence_end="2024-12-31"
)
```

### DST Handling
```python
# Handle Daylight Saving Time
spring_forward = "2024-03-10 02:00:00"
result = add_duration(spring_forward, "1 hour")
# Correctly handles DST transition

# Check DST status
info = get_timezone_info("America/New_York")
print(f"DST Active: {info['dst_active']}")
```

## Performance Optimization

### Caching
```python
# Cache timezone data
cached_timezones = {}

def get_timezone_cached(name):
    if name not in cached_timezones:
        cached_timezones[name] = get_timezone_info(name)
    return cached_timezones[name]
```

## Testing

### Unit Tests
```python
def test_timezone_conversion():
    result = convert_timezone(
        "2024-06-15 12:00:00",
        "UTC",
        "America/New_York"
    )
    assert "07:00" in result

def test_is_business_day():
    assert is_business_day("2024-06-17") == True  # Monday
    assert is_business_day("2024-06-15") == False  # Saturday
```

## Configuration

### Server Config
```python
TIME_CONFIG = {
    "default_timezone": "UTC",
    "timeformat": "%Y-%m-%d %H:%M:%S",
    "timezone_database": "olson",
    "holidays_database": "holidays"
}
```

## Dependencies
- fastmcp
- mcp
- pytz
- python-dateutil

## Use Cases
- Global team scheduling
- Event scheduling
- Reminder systems
- Meeting finders
- Timezone converters
- Business day calculations
- Holiday tracking

## Best Practices
1. Always specify timezone explicitly
2. Use UTC internally, display in user timezone
3. Be careful with DST transitions
4. Store times in UTC
5. Handle business days properly
6. Cache timezone data
7. Test edge cases (DST, year boundaries)

## Future Enhancements
- [ ] Business hours configuration
- [ ] Shift scheduling
- [ ] Calendar synchronization
- [ ] Natural language parsing
- [ ] Weather integration
- [ ] iCal support
- [ ] Multi-language support
