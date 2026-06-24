"""
utils/helpers.py
----------------
Miscellaneous helper utilities used across the application.
"""

import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


def get_current_timestamp() -> str:
    """Return the current date-time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_successful_submission(data: Dict[str, Any]) -> None:
    """
    Log a successful form submission (without sensitive data in production).

    Args:
        data (dict): The submitted form data.
    """
    timestamp = get_current_timestamp()
    logger.info(
        "[%s] Successful submission — Name: %s | Course: %s | Status: %s",
        timestamp,
        data.get("name", "N/A"),
        data.get("course", "N/A"),
        data.get("status", "N/A"),
    )


def sanitize_input(value: str) -> str:
    """
    Strip leading/trailing whitespace from a string input.

    Args:
        value (str): Raw input string.

    Returns:
        str: Sanitized string.
    """
    return value.strip() if isinstance(value, str) else value


def build_submission_data(
    name: str,
    phone: str,
    email: str,
    status: str,
    course: str,
) -> Dict[str, str]:
    """
    Build a clean dictionary of form data, sanitizing each field.

    Args:
        name, phone, email, status, course: Raw form field values.

    Returns:
        dict: Sanitized form data ready for submission.
    """
    return {
        "name":   sanitize_input(name),
        "phone":  sanitize_input(phone),
        "email":  sanitize_input(email),
        "status": sanitize_input(status),
        "course": sanitize_input(course),
    }
