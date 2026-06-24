"""
config.py
---------
Loads all configuration values from environment variables using python-dotenv.
This file centralizes all app configuration — never hardcode secrets or IDs here.
"""

import os
from dotenv import load_dotenv

# Load variables from the .env file into environment
load_dotenv()


class Config:
    """
    Central configuration class.
    All Google Form settings are loaded from environment variables.
    """

    # ── Google Form Settings ──────────────────────────────────────────────────
    GOOGLE_FORM_ACTION_URL: str = os.getenv("GOOGLE_FORM_ACTION_URL", "")
    GOOGLE_FORM_NAME_FIELD: str = os.getenv("GOOGLE_FORM_NAME_FIELD", "")
    GOOGLE_FORM_PHONE_FIELD: str = os.getenv("GOOGLE_FORM_PHONE_FIELD", "")
    GOOGLE_FORM_EMAIL_FIELD: str = os.getenv("GOOGLE_FORM_EMAIL_FIELD", "")
    GOOGLE_FORM_STATUS_FIELD: str = os.getenv("GOOGLE_FORM_STATUS_FIELD", "")
    GOOGLE_FORM_COURSE_FIELD: str = os.getenv("GOOGLE_FORM_COURSE_FIELD", "")

    # ── App Settings ──────────────────────────────────────────────────────────
    APP_TITLE: str = "SkilzLearn Admission Chatbot"
    APP_ICON: str = "🎓"
    REQUEST_TIMEOUT: int = 10   # seconds before the HTTP request times out

    # ── Dropdown Options ──────────────────────────────────────────────────────
    STATUS_OPTIONS: list = [
        "-- Select --",
        "Student",
        "Working Professional",
        "Looking  for job",
        "Others",
    ]

    COURSE_OPTIONS: list = [
        "-- Select --",
        "UI/UX design",
        "AIML",
        "AIDS",
        "Full Stack Development",
        "AI with Python",
        "Digital Marketing",
        "Cyber Security",
        "Graphics Design",
        "Cloud Computing",
    ]
