# 🎓 SkilzLearn Admission Chatbot

> **Building Bridges to Success** — A production-ready admission enquiry portal built with Python & Streamlit.

---

## 📋 Project Overview

The SkilzLearn Admission Chatbot collects prospective student information through a polished Streamlit web form, validates every field client-side, then automatically submits the data to a Google Form for CRM integration — all without any database setup.

---

## 🗂️ Project Structure

```
admission_chatbot/
│
├── app.py               # Main Streamlit application
├── config.py            # Centralised configuration (reads .env)
├── form_submitter.py    # Google Form HTTP POST logic
├── validators.py        # All field validation functions
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
├── README.md            # This file
│
├── utils/
│   ├── __init__.py
│   └── helpers.py       # Utility / helper functions
│
└── assets/
    └── logo.png         # SkilzLearn brand logo
```

---

## ⚙️ Installation & Setup

### 1. Clone / Download the project

```bash
git clone <repo-url>
cd admission_chatbot
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your Google Form values (see section below).

---

## 🔗 Google Form Configuration

### Step 1 — Create the Google Form

1. Go to [https://forms.google.com](https://forms.google.com)
2. Create a form with these **Short answer** questions:
   - Full Name
   - Phone Number
   - Email ID
   - Current Status
   - Course Interested In
3. Click **Send → Link icon** and copy the shareable link.

### Step 2 — Find the Form Action URL

1. Open the form link in Chrome.
2. Right-click the page → **Inspect** → **Network** tab.
3. Fill in dummy data and click **Submit**.
4. In the Network tab, look for a POST request to a URL like:
   `https://docs.google.com/forms/d/e/XXXXX/formResponse`
5. Copy this URL — it is your `GOOGLE_FORM_ACTION_URL`.

### Step 3 — Find the Field Entry IDs

**Method A — Pre-filled link (easiest):**
1. In your Google Form editor, click ⋮ → **Get pre-filled link**.
2. Fill each field with a recognisable placeholder (e.g. `NAME_FIELD`).
3. Click **Get link** and inspect the URL.
4. You will see query parameters like `entry.123456789=NAME_FIELD`.
5. The number after `entry.` is the field ID.

**Method B — Page source:**
1. Open the live form URL.
2. Right-click → **View Page Source**.
3. Search for `entry.` — each question has a unique `entry.XXXXXXXXX` ID.

### Step 4 — Update your .env file

```dotenv
GOOGLE_FORM_ACTION_URL=https://docs.google.com/forms/d/e/YOUR_ID/formResponse
GOOGLE_FORM_NAME_FIELD=entry.111111111
GOOGLE_FORM_PHONE_FIELD=entry.222222222
GOOGLE_FORM_EMAIL_FIELD=entry.333333333
GOOGLE_FORM_STATUS_FIELD=entry.444444444
GOOGLE_FORM_COURSE_FIELD=entry.555555555
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** by default.

---

## ✅ Validation Rules

| Field | Rules |
|-------|-------|
| Name | Required · Min 3 chars · Letters & spaces only |
| Phone | Required · Exactly 10 digits · Numbers only |
| Email | Required · Valid format (user@domain.tld) |
| Status | Required · Must select from dropdown |
| Course | Required · Must select from dropdown |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Google Form submission fails | Verify `GOOGLE_FORM_ACTION_URL` ends with `/formResponse` |
| Wrong field IDs | Re-check entry IDs using the pre-filled link method |
| Timeout errors | Check internet connection; increase `REQUEST_TIMEOUT` in `config.py` |
| Logo not showing | Ensure `assets/logo.png` exists in the project folder |

---

## 🔒 Security Notes

- **Never** commit your `.env` file to version control.
- Add `.env` to your `.gitignore`.
- The app does not store personal data in any database.

---

## 📄 License

© SkilzLearn. All rights reserved.
