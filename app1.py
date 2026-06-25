"""
app.py - SkilzLearn Admission Portal
Colorful & Vibrant UI with Animated Success Screen + AI Chatbot
"""

import os
import streamlit as st
from PIL import Image
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from config import Config
from validators import validate_all_fields
from form_submitter import submit_to_google_form
from utils.helpers import build_submission_data, log_successful_submission

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="auto",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ── Animated Background ── */
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #fff3e0 30%, #e8f5e9 60%, #fff8e1 100%);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Hide Streamlit defaults ── */
#MainMenu, footer { visibility: hidden; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; }

/* ── TOP HEADER BANNER ── */
.top-header {
    background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 40%, #e65100 100%);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 40px rgba(27,94,32,0.25);
    position: relative;
    overflow: hidden;
}
.top-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.top-header::after {
    content: '';
    position: absolute;
    bottom: -60%;
    right: 15%;
    width: 200px;
    height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.header-title {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.header-subtitle {
    color: rgba(255,255,255,0.85);
    font-size: 0.9rem;
    margin: 4px 0 0 0;
    font-weight: 400;
}
.header-badge {
    background: rgba(255,255,255,0.18);
    border: 1.5px solid rgba(255,255,255,0.3);
    border-radius: 50px;
    padding: 8px 20px;
    color: #ffffff;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    backdrop-filter: blur(10px);
}

/* ── STAT CARDS ROW ── */
.stats-row {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}
.stat-card {
    flex: 1;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.stat-card:hover { transform: translateY(-3px); }
.stat-card.green  { background: linear-gradient(135deg, #1b5e20, #43a047); }
.stat-card.orange { background: linear-gradient(135deg, #e65100, #ff8f00); }
.stat-card.teal   { background: linear-gradient(135deg, #00695c, #26a69a); }
.stat-card.purple { background: linear-gradient(135deg, #4a148c, #7b1fa2); }
.stat-number { color: #fff; font-size: 1.6rem; font-weight: 800; margin: 0; }
.stat-label  { color: rgba(255,255,255,0.85); font-size: 0.78rem; font-weight: 500; margin: 2px 0 0 0; }

/* ── WELCOME BANNER ── */
.welcome-banner {
    background: linear-gradient(135deg, #f1f8e9, #fff9c4, #fce4ec);
    border: 2px solid #a5d6a7;
    border-radius: 14px;
    padding: 16px 24px;
    margin-bottom: 22px;
    text-align: center;
    font-size: 1rem;
    font-weight: 600;
    color: #1b5e20;
    box-shadow: 0 3px 12px rgba(165,214,167,0.3);
    animation: pulseWelcome 3s ease-in-out infinite;
}
@keyframes pulseWelcome {
    0%, 100% { box-shadow: 0 3px 12px rgba(165,214,167,0.3); }
    50%       { box-shadow: 0 6px 24px rgba(165,214,167,0.5); }
}

/* ── FORM CARD ── */
.form-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 36px 40px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    border-top: 5px solid transparent;
    border-image: linear-gradient(90deg, #2e7d32, #e65100) 1;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
}

/* ── Section Titles ── */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1b5e20;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-sub {
    font-size: 0.83rem;
    color: #9e9e9e;
    margin-bottom: 18px;
    margin-left: 2px;
}

/* ── Input Styling ── */
.stTextInput label, .stSelectbox label {
    font-weight: 600 !important;
    color: #2e7d32 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.2px !important;
}
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 2px solid #c8e6c9 !important;
    padding: 11px 16px !important;
    font-size: 0.95rem !important;
    background: #f9fbe7 !important;
    transition: all 0.25s ease !important;
    font-family: 'Poppins', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2e7d32 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 4px rgba(46,125,50,0.1) !important;
}
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 2px solid #c8e6c9 !important;
    background: #f9fbe7 !important;
}

/* ── Error messages ── */
.field-error {
    background: #fff5f5;
    border-left: 3px solid #ef5350;
    border-radius: 6px;
    color: #c62828;
    font-size: 0.82rem;
    padding: 6px 12px;
    margin-bottom: 8px;
    font-weight: 500;
}

/* ── Divider ── */
.fancy-divider {
    height: 3px;
    background: linear-gradient(90deg, #2e7d32, #e65100, #2e7d32);
    border-radius: 2px;
    border: none;
    margin: 22px 0;
}

/* ── Submit Button ── */
.stButton > button {
    background: linear-gradient(135deg, #1b5e20, #2e7d32, #e65100) !important;
    background-size: 200% 200% !important;
    animation: btnGradient 3s ease infinite !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 40px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    margin-top: 16px !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 6px 20px rgba(27,94,32,0.35) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    font-family: 'Poppins', sans-serif !important;
}
@keyframes btnGradient {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(27,94,32,0.45) !important;
}

/* ── ANIMATED SUCCESS SCREEN ── */
.success-wrapper {
    text-align: center;
    padding: 20px;
    animation: fadeInUp 0.6s ease forwards;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
.success-circle {
    width: 110px;
    height: 110px;
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
    border-radius: 50%;
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    box-shadow: 0 0 0 12px rgba(46,125,50,0.12), 0 0 0 24px rgba(46,125,50,0.06);
    animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.2s both;
}
@keyframes popIn {
    from { transform: scale(0); }
    to   { transform: scale(1); }
}
.success-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: #1b5e20;
    margin-bottom: 10px;
}
.success-message {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border: 2px solid #a5d6a7;
    border-radius: 14px;
    padding: 20px 28px;
    font-size: 1rem;
    font-weight: 600;
    color: #2e7d32;
    margin: 16px auto;
    max-width: 500px;
    box-shadow: 0 4px 16px rgba(46,125,50,0.12);
}
.success-confetti {
    font-size: 2rem;
    animation: bounce 1s ease infinite;
    display: inline-block;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
}
.success-steps {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
    flex-wrap: wrap;
}
.success-step {
    background: #ffffff;
    border: 2px solid #c8e6c9;
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #388e3c;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    animation: fadeInUp 0.5s ease forwards;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 50%, #e65100 100%) !important;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
.sidebar-card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
}
.sidebar-card h4 {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
    color: #ffcc02 !important;
}
.sidebar-card p, .sidebar-card li {
    font-size: 0.83rem;
    line-height: 1.7;
    margin: 0;
}
.sidebar-card ul { padding-left: 14px; margin: 0; }
.course-chip {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    margin: 3px 2px;
    font-weight: 500;
}

/* ── CHATBOT STYLES ── */
.chatbot-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.10);
    margin-top: 28px;
    border-top: 5px solid;
    border-image: linear-gradient(90deg, #1b5e20, #e65100) 1;
}
.chatbot-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}
.chatbot-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #1b5e20;
    margin: 0;
}
.chatbot-subtitle {
    font-size: 0.82rem;
    color: #9e9e9e;
    margin: 2px 0 0 0;
}
.chat-bubble-user {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    font-size: 0.9rem;
    font-weight: 500;
    width: fit-content;
    margin-left: auto;
}
.chat-bubble-ai {
    background: linear-gradient(135deg, #f1f8e9, #e8f5e9);
    color: #1b5e20;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    margin: 8px auto 8px 0;
    max-width: 80%;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1.5px solid #c8e6c9;
    width: fit-content;
}
.chat-avatar-ai {
    font-size: 1.4rem;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Gemini AI Chatbot ─────────────────────────────────────────────────────────
def get_smart_reply(user_input: str, course: str, name: str) -> str:
    try:
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are helpful AI Assistant.

Student Name: {name}
Course: {course}

Rules:
- Answer Computer Science, Programming, AI, Cyber Security, Cloud Computing, Data Science, Full Stack Development, UI/UX, and Technology related questions.
- AILM means Artificial intelligence and Machine Learning.
- AIDs means artificial intelligence and Data Science.
- Give clear and accurate answers.
- Use simple English.
- Explain concepts in an easy-to-understand way.
- Keep answers between 50 and 150 words.
- If the question is not related to Computer Science or Technology, politely say:
  "I am designed to answer Computer Science and Technology related questions only."
- Do not add unnecessary information.
- Do not mention fees, certificates, placements, duration, or syllabus unless asked.
"""                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Sorry, AI service unavailable.Error: {str(e)}"
# ── Session State ──────────────────────────────────────────────────────────────
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "form_key" not in st.session_state:
    st.session_state.form_key = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "submitted_course" not in st.session_state:
    st.session_state.submitted_course = ""
if "submitted_name" not in st.session_state:
    st.session_state.submitted_name = ""

def reset_form():
    st.session_state.submitted = False
    st.session_state.form_key += 1
    st.session_state.chat_history = []
    st.session_state.submitted_course = ""
    st.session_state.submitted_name = ""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            st.image(Image.open(logo_path), use_container_width=True)
        except Exception:
            st.markdown("**🎓 SKILZLEARN**")
    else:
        st.markdown("**🎓 SKILZLEARN**")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card">
            <h4>🎓 Courses</h4>
            <span class="course-chip">UI/UX design</span>
            <span class="course-chip">AIML</span>
            <span class="course-chip">AIDS</span>
            <span class="course-chip">Full Stack Development</span>
            <span class="course-chip">AI with Python</span>
            <span class="course-chip">Digital Marketing</span>
            <span class="course-chip">Graphics Design</span>
            <span class="course-chip">Cyber Security</span>
            <span class="course-chip">Cloud Computing</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card">
            <h4>✅ How It Works</h4>
            <p>① Fill your details<br>
               ② Select your course<br>
               ③ Click Submit<br>
               ④ We contact you!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card">
            <h4>📞 Contact</h4>
            <p>📧 admissions@skilzlearn.com<br>
               📱 +91-XXXXXXXXXX<br>
               🌐 www.skilzlearn.com</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card">
            <h4>🕐 Office Hours</h4>
            <p>Mon–Sat: 9 AM – 7 PM<br>
               Sunday: Closed</p>
        </div>
    """, unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────

# Top Header with Logo
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
col_logo, col_text = st.columns([1, 3])
with col_logo:
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path)
            st.image(logo_img, use_container_width=True)
        except Exception:
            st.markdown("🎓", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background:linear-gradient(135deg,#1b5e20,#e65100);
                border-radius:12px;padding:20px;text-align:center;color:white;
                font-size:1.4rem;font-weight:800;">
                SKILZLEARN
            </div>
        """, unsafe_allow_html=True)
with col_text:
    st.markdown("""
        <div style="padding-top:16px;">
            <h1 style="color:#1b5e20;font-size:2rem;font-weight:800;margin:0 0 4px 0;">
                Admission Portal
            </h1>
            <p style="color:#e65100;font-size:0.95rem;margin:0;font-weight:500;">
                🌟 Building Bridges to Success — Start Your Journey Today!
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Stats Row
st.markdown("""
    <div class="stats-row">
        <div class="stat-card green">
            <p class="stat-number">6+</p>
            <p class="stat-label">Courses Available</p>
        </div>
        <div class="stat-card orange">
            <p class="stat-number">500+</p>
            <p class="stat-label">Students Enrolled</p>
        </div>
        <div class="stat-card teal">
            <p class="stat-number">95%</p>
            <p class="stat-label">Placement Rate</p>
        </div>
        <div class="stat-card purple">
            <p class="stat-number">24h</p>
            <p class="stat-label">Response Time</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Welcome Banner
st.markdown("""
    <div class="welcome-banner">
        👋 Welcome! Please fill in your details below — our admissions team will contact you within 24 hours!
    </div>
""", unsafe_allow_html=True)

# ── SUCCESS SCREEN ────────────────────────────────────────────────────────────
if st.session_state.submitted:
    st.markdown("""
        <div class="success-wrapper">
            <div class="success-circle">✅</div>
            <div class="success-title">Registration Successful! 🎉</div>
            <div class="success-message">
                ✅ Thank you for registering.<br>
                Our administration team will contact you soon.
            </div>
            <div>
                <span class="success-confetti" style="animation-delay:0s">🎊</span>
                <span class="success-confetti" style="animation-delay:0.2s">⭐</span>
                <span class="success-confetti" style="animation-delay:0.4s">🎓</span>
                <span class="success-confetti" style="animation-delay:0.6s">⭐</span>
                <span class="success-confetti" style="animation-delay:0.8s">🎊</span>
            </div>
            <div class="success-steps">
                <div class="success-step">📧 Check your email</div>
                <div class="success-step">📱 Watch for our call</div>
                <div class="success-step">🚀 Get ready to learn!</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── AI CHATBOT SECTION ────────────────────────────────────────────────────
    st.markdown("""
        <div class="chatbot-container">
            <div class="chatbot-header">
                <span style="font-size:2rem;">🤖</span>
                <div>
                    <p class="chatbot-title">SkilzLearn AI Assistant</p>
                    <p class="chatbot-subtitle">Ask me anything about your course, fees, schedule, or career prospects!</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Show initial greeting if no chat yet
    if not st.session_state.chat_history:
        course = st.session_state.submitted_course
        name = st.session_state.submitted_name
        greeting = f"Hi {name}! 👋 Congratulations on registering for **{course}** at SkilzLearn! I'm your AI assistant. You can ask me anything — course syllabus, duration, fees, placement support, career paths, or any other questions you have. How can I help you today?"
        st.session_state.chat_history.append({"role": "assistant", "content": greeting})

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.chat_input("Ask your question here... (e.g. What is the course duration?)")

    if user_input and user_input.strip():
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Build Anthropic messages (skip system prompt, use user/assistant turns)
        course = st.session_state.submitted_course
        name = st.session_state.submitted_name

        # ── Rule-based AI chatbot (no API needed) ──
        ai_reply = get_smart_reply(user_input.strip(), course, name)

        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.rerun()

    # Register Another button
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
    with col_btn2:
        if st.button("📝  Register Another Enquiry"):
            reset_form()
            st.rerun()

# ── FORM ──────────────────────────────────────────────────────────────────────
else:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # Section 1 — Personal Details
    st.markdown("""
        <div class="section-title">👤 Personal Details</div>
        <div class="section-sub">All fields are mandatory. Your data is safe with us 🔒</div>
    """, unsafe_allow_html=True)

    k = st.session_state.form_key

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Rohit Sharma", key=f"name_{k}")
    with col2:
        phone = st.text_input("Phone Number", placeholder="10-digit mobile number", max_chars=10, key=f"phone_{k}")

    email = st.text_input("Email ID", placeholder="e.g. iyyaps@example.com", key=f"email_{k}")

    # Divider
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # Section 2 — Course Preference
    st.markdown("""
        <div class="section-title">🎓 Course Preference</div>
        <div class="section-sub">Tell us what you want to learn and where you are now</div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        status = st.selectbox("Current Status", options=Config.STATUS_OPTIONS, key=f"status_{k}")
    with col4:
        course = st.selectbox("Course Interested In", options=Config.COURSE_OPTIONS, key=f"course_{k}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Submit Button
    submit_clicked = st.button("🚀  Submit", key=f"submit_{k}")

    if submit_clicked:
        validation = validate_all_fields(name, phone, email, status, course)

        if not validation["is_valid"]:
            st.markdown("<br>", unsafe_allow_html=True)
            for field, msg in validation["errors"].items():
                label = {"name":"Full Name","phone":"Phone Number","email":"Email ID",
                         "status":"Current Status","course":"Course Interested In"}.get(field, field.title())
                st.markdown(f'<div class="field-error">❌ <b>{label}:</b> {msg}</div>', unsafe_allow_html=True)
        else:
            form_data = build_submission_data(name, phone, email, status, course)
            with st.spinner("✨ Submitting your enquiry... please wait!"):
                result = submit_to_google_form(form_data)

            if result["success"]:
                log_successful_submission(form_data)
                st.session_state.submitted = True
                st.session_state.submitted_course = course
                st.session_state.submitted_name = name
                st.rerun()
            else:
                st.error(f"⚠️ Submission failed: {result['message']}")
                st.info("💡 Please try again or contact us at admissions@skilzlearn.com")
