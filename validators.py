"""
validators.py
-------------
Contains all validation logic for the admission chatbot form fields.
Each function returns a tuple: (is_valid: bool, error_message: str)
"""

import re
from typing import Tuple


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate the user's name.
    Rules:
        - Cannot be empty
        - Minimum 3 characters
        - Only alphabets and spaces allowed
    """
    name = name.strip()
    if not name:
        return False, "Name cannot be empty."
    if len(name) < 3:
        return False, "Name must be at least 3 characters long."
    if not re.match(r"^[A-Za-z\s]+$", name):
        return False, "Name can only contain letters and spaces."
    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate the phone number.
    Rules:
        - Must be exactly 10 digits
        - Only numeric characters allowed
    """
    phone = phone.strip()
    if not phone:
        return False, "Phone number cannot be empty."
    if not phone.isdigit():
        return False, "Phone number must contain only digits."
    if len(phone) != 10:
        return False, "Phone number must be exactly 10 digits."
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate the email address.
    Rules:
        - Must follow standard email format (user@domain.tld)
    """
    email = email.strip()
    if not email:
        return False, "Email ID cannot be empty."
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(pattern, email):
        return False, "Please enter a valid email address (e.g. user@example.com)."
    return True, ""


def validate_status(status: str) -> Tuple[bool, str]:
    """
    Validate current status selection.
    Rules:
        - Must be selected (cannot be empty/placeholder)
    """
    if not status or status == "-- Select --":
        return False, "Please select your current status."
    return True, ""


def validate_course(course: str) -> Tuple[bool, str]:
    """
    Validate course selection.
    Rules:
        - Must be selected (cannot be empty/placeholder)
    """
    if not course or course == "-- Select --":
        return False, "Please select a course you are interested in."
    return True, ""


def validate_all_fields(name: str, phone: str, email: str, status: str, course: str) -> dict:
    """
    Run all validations and return a dict with results.

    Returns:
        dict with keys: 'is_valid' (bool) and 'errors' (dict of field -> error msg)
    """
    errors = {}

    name_valid, name_err = validate_name(name)
    if not name_valid:
        errors["name"] = name_err

    phone_valid, phone_err = validate_phone(phone)
    if not phone_valid:
        errors["phone"] = phone_err

    email_valid, email_err = validate_email(email)
    if not email_valid:
        errors["email"] = email_err

    status_valid, status_err = validate_status(status)
    if not status_valid:
        errors["status"] = status_err

    course_valid, course_err = validate_course(course)
    if not course_valid:
        errors["course"] = course_err

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
