import re
from typing import Optional, Dict, Any

class ValidationException(Exception):
    """Custom exception for validation errors."""
    pass

def validate_registration_payload(payload: Dict[str, Any]) -> None:
    """
    Validates the data payload for new content registration.

    :param payload: The data dictionary from the user request.
    :raises ValidationException: If any required field is missing or invalid.
    """
    required_fields = ['title', 'content', 'wallet_address']
    
    for field in required_fields:
        if field not in payload or not payload[field]:
            raise ValidationException(f"Missing required field: {field}")

    # Basic content length check
    if len(payload['content']) < 50:
        raise ValidationException("Content must be at least 50 characters long.")

    # Basic Solana wallet address format check (Public Key length)
    if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', payload['wallet_address']):
        raise ValidationException("Invalid Solana wallet address format.")

def validate_url(url: str) -> Optional[str]:
    """
    Performs a basic check on a URL string.
    
    :param url: The URL to check.
    :return: The cleaned URL if valid, otherwise raises an exception.
    """
    # Simple regex for URL pattern matching
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if re.match(url_pattern, url):
        return url.strip()
    else:
        raise ValidationException(f"Invalid URL format: {url}")