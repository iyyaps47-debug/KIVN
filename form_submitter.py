"""
form_submitter.py
-----------------
Handles the HTTP POST submission to Google Forms.
Uses the requests library and reads config from environment variables.
"""

import logging
import requests
from typing import Dict, Any

from config import Config

# Configure a logger for this module
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)


def submit_to_google_form(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit admission form data to a Google Form via HTTP POST.

    Args:
        data (dict): Keys are field names collected from the UI:
                     'name', 'phone', 'email', 'status', 'course'

    Returns:
        dict with keys:
            'success' (bool)   – True if submission was accepted
            'message' (str)    – Human-readable result or error description
    """

    # ── Pre-flight checks ─────────────────────────────────────────────────────
    if not Config.GOOGLE_FORM_ACTION_URL:
        logger.error("GOOGLE_FORM_ACTION_URL is not set in environment.")
        return {
            "success": False,
            "message": (
                "Google Form URL is not configured. "
                "Please set GOOGLE_FORM_ACTION_URL in your .env file."
            ),
        }

    required_fields = [
        Config.GOOGLE_FORM_NAME_FIELD,
        Config.GOOGLE_FORM_PHONE_FIELD,
        Config.GOOGLE_FORM_EMAIL_FIELD,
        Config.GOOGLE_FORM_STATUS_FIELD,
        Config.GOOGLE_FORM_COURSE_FIELD,
    ]
    if not all(required_fields):
        logger.error("One or more Google Form field IDs are missing.")
        return {
            "success": False,
            "message": (
                "Google Form field IDs are not fully configured. "
                "Please check your .env file."
            ),
        }

    # ── Build the POST payload ────────────────────────────────────────────────
    payload = {
        Config.GOOGLE_FORM_NAME_FIELD:   data.get("name", ""),
        Config.GOOGLE_FORM_PHONE_FIELD:  data.get("phone", ""),
        Config.GOOGLE_FORM_EMAIL_FIELD:  data.get("email", ""),
        Config.GOOGLE_FORM_STATUS_FIELD: data.get("status", ""),
        Config.GOOGLE_FORM_COURSE_FIELD: data.get("course", ""),
    }

    logger.info("Submitting form data to Google Form: %s", Config.GOOGLE_FORM_ACTION_URL)

    # ── HTTP POST with comprehensive error handling ───────────────────────────
    try:
        response = requests.post(
            Config.GOOGLE_FORM_ACTION_URL,
            data=payload,
            timeout=Config.REQUEST_TIMEOUT,
            # Google Forms redirects to a confirmation page; we don't follow it
            allow_redirects=True,
        )

        # Google Forms returns 200 on the confirmation page after redirect
        if response.status_code in (200, 302):
            logger.info("Form submitted successfully. Status code: %s", response.status_code)
            return {"success": True, "message": "Form submitted successfully."}

        # Any unexpected status code
        logger.warning("Unexpected response status: %s", response.status_code)
        return {
            "success": False,
            "message": (
                f"Unexpected server response (HTTP {response.status_code}). "
                "Please try again later."
            ),
        }

    except requests.exceptions.ConnectionError:
        logger.error("Connection error while submitting to Google Form.")
        return {
            "success": False,
            "message": (
                "Network connection failed. "
                "Please check your internet connection and try again."
            ),
        }

    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds.", Config.REQUEST_TIMEOUT)
        return {
            "success": False,
            "message": (
                f"The request timed out after {Config.REQUEST_TIMEOUT} seconds. "
                "Please try again."
            ),
        }

    except requests.exceptions.InvalidURL:
        logger.error("Invalid Google Form URL: %s", Config.GOOGLE_FORM_ACTION_URL)
        return {
            "success": False,
            "message": (
                "The Google Form URL appears to be invalid. "
                "Please verify GOOGLE_FORM_ACTION_URL in your .env file."
            ),
        }

    except requests.exceptions.RequestException as exc:
        logger.exception("Unexpected requests error: %s", exc)
        return {
            "success": False,
            "message": f"An unexpected network error occurred: {exc}",
        }

    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unexpected error during form submission: %s", exc)
        return {
            "success": False,
            "message": f"An unexpected error occurred: {exc}",
        }
