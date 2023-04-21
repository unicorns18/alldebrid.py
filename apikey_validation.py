"""
This module contains a function to validate API keys.
"""
# Temporary file to validate API keys
import re


def check_if_valid_key(api_key: str) -> bool:
    """
    Shiver me timbers! This method takes an API key string and checks if it matches the format of a valid key.

    Parameters:
    -----------
    - api_key (str): The API key to be checked.

    Returns:
    --------
    - bool: True if the key matches the format, False otherwise.
    """
    if not isinstance(api_key, (str, bytes)):
        raise ValueError("API key must be a str or bytes-like object.")

    key_pattern = re.compile(r'^[a-zA-Z0-9]{20}$')

    if key_pattern.match(api_key):
        return True
    else:
        return False
