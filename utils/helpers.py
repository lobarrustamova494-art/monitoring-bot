"""Helper functions"""
import re
from typing import Optional

def parse_channel_username(input_text: str) -> Optional[str]:
    """
    Parse channel username from various input formats
    
    Examples:
        @channelname -> channelname
        https://t.me/channelname -> channelname
        t.me/channelname -> channelname
        channelname -> channelname
    """
    input_text = input_text.strip()
    
    # Remove @ prefix
    if input_text.startswith("@"):
        return input_text[1:]
    
    # Extract from URL
    url_pattern = r"(?:https?://)?(?:www\.)?t(?:elegram)?\.me/([a-zA-Z0-9_]+)"
    match = re.match(url_pattern, input_text)
    if match:
        return match.group(1)
    
    # Return as is if valid username format
    if re.match(r"^[a-zA-Z0-9_]{5,}$", input_text):
        return input_text
    
    return None

def format_number(num: int) -> str:
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text
