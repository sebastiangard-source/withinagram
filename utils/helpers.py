# utils/helpers.py

import re
#from datetime import datetime
from dateutil import parser

def sanitize_username(username):
    """Sanitize a username by removing disallowed characters and normalizing."""
    if not username:
        return None
    return re.sub(r'[^a-zA-Z0-9_-]', '', username.strip().replace(" ", "").lower())

def get_rest_headers(api_key):
    """Return headers used for Supabase REST API requests."""
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def format_timestamp(iso_timestamp):
    """Convert ISO timestamp to a friendlier datetime format."""
    try:
        dt = parser.isoparse(iso_timestamp)
        return dt.strftime('%b %d, %Y %I:%M %p')
    except Exception:
        return iso_timestamp  # fallback if parsing fails

def truncate_text(text, limit=30):
    """Shorten text if it exceeds a character limit."""
    return text if len(text) <= limit else text[:limit] + "..."
