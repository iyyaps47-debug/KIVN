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

/* ── Background ── */
.stApp {
    background: #ffffff;
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
    background: #ffffff !important;
    border-right: 2px solid #e8f5e9 !important;
}
[data-testid="stSidebar"] * { color: #1b5e20 !important; }

/* Card base */
.sidebar-card {
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

/* Courses — deep green */
.card-courses {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
}
.card-courses * { color: #ffffff !important; }
.card-courses h4 { color: #ffeb3b !important; }

/* How It Works — orange */
.card-howitworks {
    background: linear-gradient(135deg, #e65100, #ff8f00);
}
.card-howitworks * { color: #ffffff !important; }
.card-howitworks h4 { color: #fff9c4 !important; }

/* Main Branch — teal green */
.card-branch {
    background: linear-gradient(135deg, #004d40, #00897b);
}
.card-branch * { color: #ffffff !important; }
.card-branch h4 { color: #b2dfdb !important; }

/* Contact — orange-red */
.card-contact {
    background: linear-gradient(135deg, #bf360c, #e64a19);
}
.card-contact * { color: #ffffff !important; }
.card-contact h4 { color: #ffccbc !important; }
.card-contact a { color: #ffeb3b !important; }

/* Office Hours — dark green */
.card-hours {
    background: linear-gradient(135deg, #33691e, #558b2f);
}
.card-hours * { color: #ffffff !important; }
.card-hours h4 { color: #f0f4c3 !important; }

.sidebar-card h4 {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.sidebar-card p, .sidebar-card li {
    font-size: 0.83rem;
    line-height: 1.7;
    margin: 0;
}
.sidebar-card ul { padding-left: 14px; margin: 0; }
.course-chip {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    margin: 3px 2px;
    font-weight: 500;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.3);
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



/* ── PARTNER LOGOS ── */
.partner-logos {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-shrink: 0;
}
.logos-img {
    height: 100px;
    width: auto;
    max-width: 500px;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
}

/* ── TYPING INDICATOR ── */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 12px 18px;
    background: linear-gradient(135deg, #f1f8e9, #e8f5e9);
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
    border: 1.5px solid #c8e6c9;
    margin: 8px 0;
    font-size: 0.85rem;
    color: #2e7d32;
    font-weight: 500;
}
.typing-dot {
    width: 7px; height: 7px;
    background: #2e7d32;
    border-radius: 50%;
    display: inline-block;
    animation: typingBounce 1.2s ease infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-5px); opacity: 1; }
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
- AIML means Artificial intelligence and Machine Learning.
- AIDs means artificial intelligence and Data Science.
- Give clear and accurate answers.
- Use simple English.
- Explain concepts in an easy-to-understand way.
- Keep answers between 150 and 350 words.
- If the question is not related to Computer Science or Technology, respond politely:
"Sorry, I can only assist with Computer Science, Programming, AI, Data Science, Cyber Security, Cloud Computing, and other technology-related topics. Please ask a technology-related            question, and I'll be happy to help."
- Do not add unnecessary information.
- If the user asks about course duration answer the question.
- Do not mention fees, certificates, placements,syllabus unless asked.
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
if "submitted_email" not in st.session_state:
    st.session_state.submitted_email = ""
if "submitted_message" not in st.session_state:
    st.session_state.submitted_message = ""
if "typing" not in st.session_state:
    st.session_state.typing = False

def reset_form():
    st.session_state.submitted = False
    st.session_state.form_key += 1
    st.session_state.chat_history = []
    st.session_state.submitted_course = ""
    st.session_state.submitted_name = ""
    st.session_state.submitted_email = ""
    st.session_state.submitted_message = ""
    st.session_state.show_email = False
    st.session_state.typing = False

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            st.image(Image.open(logo_path), use_container_width=True)
        except Exception:
            st.markdown("**🎓 LearnMate**")
    else:
        st.markdown("**🎓 LearnMate**")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card card-courses">
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
        <div class="sidebar-card card-howitworks">
            <h4>✅ How It Works</h4>
            <p>👉 Fill your details<br>
               👉 Select your course<br>
               👉 Click Submit<br>
               👉 We contact you!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card card-branch">
            <h4>📍 Main Branch</h4>
            <p>Second Floor, Aruna Avanthika Building,<br>
               280-3/4, B4, NSR Rd, Saibaba Colony,<br>
               Coimbatore, Tamil Nadu 641025</p>
            <a href="https://maps.google.com/?q=Aruna+Avanthika+Building+NSR+Rd+Saibaba+Colony+Coimbatore+Tamil+Nadu+641025"
               target="_blank"
               style="display:inline-block;margin-top:8px;background:rgba(255,255,255,0.2);
                      color:#fff !important;padding:5px 14px;border-radius:20px;
                      font-size:0.75rem;font-weight:600;text-decoration:none;
                      border:1px solid rgba(255,255,255,0.4);">
                🗺️ Open in Google Maps
            </a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card card-contact">
            <h4>📞 Contact Us</h4>
            <p>📧 skilzlearn.gpc@gmail.com<br>
               📧 info@skilzlearn.com<br>
               📱 +91 9787000027<br>
               🌐 <a href="https://www.skilzlearn.com" target="_blank">www.skilzlearn.com</a></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card card-hours">
            <h4>🕐 Office Hours</h4>
            <p>Mon – Sat: 9:30 AM – 7:00 PM<br>
               Closed on Sundays &amp; Public Holidays</p>
        </div>
    """, unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────

# Top Header with Logo
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
col_logo, col_text, col_logos = st.columns([1.2, 3.5, 1.3])
with col_logo:
    st.empty()  # Logo removed from main header
with col_text:
    st.markdown("""
        <div style="padding-top:16px;">
            <h1 style="color:#1b5e20;font-size:3.5rem;font-weight:800;margin:0 0 4px 0;letter-spacing:-1px;">
                LearnMate
            </h1>
            <p style="color:#e65100;font-size:0.95rem;margin:0;font-weight:500;">
                🌟 Building Bridges to Success — Start Your Journey Today!
            </p>
        </div>
    """, unsafe_allow_html=True)
with col_logos:
    st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:flex-end;
                    height:100%;padding-top:0px;margin-top:-60px">
            <img src="data:image/jpeg;base64,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AAAAAAAAAAAAYyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMGQAGMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//8QAAv/aAAwDAQACAAMAAAAhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/EAAL/2gAMAwEAAgADAAAAEHPNPLDPPHMLAIDHPLPIDFJDPDPJDKJPLOFKIMLBNDDDPNPHONPPPENPPMLDMPCAELHMFHPMPHPCPPCHPHNLHPNKPLECPPLMMPPDPBOPNPMPEMHNKEMGLPBDAIBHLPPJDGJOPIADBCMEBOADAPJNAAGOBOEIFJLCPLAAABOIAAFOMMMPONEDENONMECOMBPGKJKAIAAMPELODCNCFDBPKEAAPOPJMODAOAFMLKABPLDCPGIBPNDFMCADDDACCLDAECADMNAFBBAAEENDDBCBHPPECEDOHCDLPPPDBDHINNHPLPPCFFPCEPIAAEMMMIBMAECAAEMNPPAEPMLELAAMCDBCAGINPPPIAAACAEEAKENAAAFOAEOMEMKADBIFEGAGALOIEOJDDPMEMBGEIPPOIAFAHAKEIAANAAAABBCACDAEAAAEACEJEKAFDAPPLCLAAANCGMFLAEBABCDAICABFOBCGBABABPMPDKAAGCBFDEPAPCDCAMJHPPMAOAAAAAEACIAAABECPBBCIALGBACLDDONCDIAAAPOAMMLIFDCANPDGMFLBEEDPHABACEMIAADAAHPPOIBHLKEAIDCABH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GICAKMAPMMLEBOAAJHPLCBOMAADFLPBPLJk9+sL8W3iFFWZCBBGLCBAMIAJBCJDCBDCAPAAENANCJBDFOAICDAAFBDAACCAKDKALOAAHCIBHHOMIBENNKEEOEMCPJHBHMMMIAPAAOEAAIFEFOAABAFAMMMJJAFFLAAAJAEOEOAMAAGIAHMIIBAADOLBEMIJPCDIBCAAFHIACAEBHMBOLCBHCIBJAELEIDDACADAIIAAAAAAIDADAADAAABAEIALAFAMKAPDDDPKAAAAEIBABEAAADIBACIAFAMANMEIJFCFMBCAEABDDNFDGDEENFDCAGIBAGNCAAJAAAAAIDCGKJLABACEMAEIAGEJDNBPDNDMNDPGMAFMCAAAADGACCEBLMMBKEMAAAMAJMKABEOAMNONPLAECAIAEIAAEJAEIAAAACMKDMBABGMCAAABMIBAMEABAACEEAFPPOPPPOBKAAEBFAIBEBDCLHLPDABAACFBABIAHPIFAABADEAMIOAJEIINLCAAEIFDLAAAEEIAFAFBCADCAAIBECAAAEEAEADOIIEMNDHPDCEMJPAAFLDABPIBFPPMEHDFENMIIGEAAOIFKAEABADEPOPLLHHIDBDCDGAAOMNIPPKAOLLLGIBAMICANLHDHBEMAAGBAOFGLAEMMAEMJEPAEJPKEAFGPPIHMMMCACMMFFOELDJCAIGBCHPJHLPPIACFPDAJCAGAJGJGAEACAAGEAIAHIBJLBAEJABPPFGIFAAAAANIADFBAIAAAAHAAAAACNIAFAAEIMEAADBAMBKAMEAAAAFOAGNPGAAPAALLAAAICJAAMMAAAFIAMMAAAAOAMAMIAAGEMGFIAIEIEDDKPMNBAFABAKAAAAAJFOHNPAAABAAABDAKIAAAMAAAAIAAADEEIGACBCAIABABEGCBLAOKACABBIBAJADBCABPBBOALCMMMAACAAEAEFIAENFAGAHMAACBLLPDJDDDPMAADECJCAIEDFKMCLCCMBLOMMAEAJCAEDDCIABAFPPAICBBBIANMCAAAABIAAGBDDHMCAJAAACBKDADFDFFKCEIBMMAAKAKNDPDMIOOEIBMAMEIPPDCELAHAJAHKCHAAAABAHMKAAIBHPPDOBCEADDGIOGAELHLDCJNACANLCAMDLBCEFLDCADMPLDDEADDKACIGDPGJCAILAIAHNLDAHBCDDFKAHNLDPONAEIAEANPMOODCBCAENGEAAELCAAEAADGEBMMJGAPBMHGAPGMNNAEKLDAEMMAMABOBABAAADOEMIEPDAPOJAJGIBGAMPPAJPDCAMABMMPPDEOIBCHCAFCEKCCPDLMAADDBAEIAAADBKIEMDDBCBCIAAFOHCCBMACADHMOLACBFGCBABFHOIAAADLCDHKMNKEIFPMIAMJMMNJEIIAIENIFKNMNPIEMJMMIAEIINECAMIEBEOEINOIBFBCALGIMCKAMIEJCAMJMLABNMMMMIAAANMAMJNMMMKHMMMAEOMMP/EAEoRAAIBAwIEAQcGCwYFBAMAAAECAwAEERIhBTFBURMGEBQiMmFxFSAjMIGRM0JQUlVikqHB0eEHJFNgcrFAQ3OCsjRUkKCiwtL/2gAIAQIBAT8A/wDnyZlUEsQAOZNel2/SQH4Amo54pPYcH/gQCTgAk0bW5CFzC4UdSKRHdgqKSx5AVJbzx+3E6/EH/JstzhtKFQAN3PIe6ri7dkMbJp9baT8U6Dk/7UZkiMoYROQhxnuKt5RHKkmQ2VOy88HrvXpMmnxAF06sBD7R+FI6uMqQfrURndVUZJOBS8FVYvpZ1EjD1RnarY2ljLraYyOARpQbffS8WupC6mJXQgjTio77QfEjso1Iz6wqLi7ssiXOcMpAZRuM1BYW0r6hdqY+ufVar3hctsviBg8ff/JUxcRuUGWxsKWUNEU0n1GDAHOT99FiGQtjBb1iNsa8jOftpXjjaQPIEYHGD3+4jFRuTEwXGnVkMTuQnuPTeiTHLrI3RyccvxOlcOleSSVtDAHdie/b6y0tJbqUIg+J6AVJY29lJrll1AH1UGzE1cSSXMplcAZHsjtWiJY2Vjvq2NI6hdLZ9rORQkAC5VsqCB23rVGwG+DhV+HepIkOCm2QD8BUU6GFbS4JCc1demaPBvotYuFY53077UwAYgHODz+si4bdyDUUCL+c50ijZ2cf4S+Unsilq0cKHOSc/ACvD4U3KeZfioNDh8Un4G8iY9m9U1NaXMH4SMgd+Y+tXGRnlXEeHJaxxSRuWR+p+8ee1gNxPHEPxmwT2FcRtYrWcRRuzeqCc9z+RuIRxrcREdy5GdtquQCqx88bEcskDP8AGlQFVIzpBGAcNtv1PStZSQOXLMQFJPbGMUhDzQtnYsobpudqiiSJAiDAH1aIzsqqMknAFWPjWKXEsoZVxpCHYs1RJqbW5O+4PPJ7Gpp4o0dtQVEBJdttArifloiMY+HxB8beNJy+xan8oeNzn17+YDsh0L9y4ocV4mp1Lf3APcSNVn5W8Zt8eJMJ16rKMn9rnXBvKOx4liNfopyMeC59r/SetDR4ZJ5A7jua4VdiCVlY4WQYB6A9DU9tco0jSI2zbtjbJ+qt7F5F8WRhHF1duvwo3sFuNNpEM/4r7t9navRry5CPNMqh/ZLtz+Arw1hnZJ1J0kghT1q+itYRGsUTZdFcMWzzqeCNLa1cA6nDFvsNPZQJHFquNDsgbDKcb++oLm7iDeGzFR7QO61myu9mAgl7j2D/ACqe2lgfTIuOx6H4fVcQnu7eSOVBmIbMKt7iO4jWSM5Bq2BveDPFzaPIHxG4rg3DorjXLKMqpwF7mr/hVrJCxijCOBtgVwGBdUs78lGkVdTGaeWU/jMTUt1JJMscHfdvyLxaJ8RyryU4f4ZBqRjkPggcz/uO1REhB7mH3jb+FGQGRASNiCR7hVnEZriJQTgbt8B0P1nBvC9Ky7YbHqfGruee6nZZHA0s2kHlThoQwdwqhSz55KB1NeUPH5OJTGKIstqh9ReRY/nN5uD8F4jxi69Hs49RG7MdlQd2NWlhBbW1nY29lEbRoV15QEPkbl68ouGjhvF7qBIysJkZoOxiJOkigzKQQxBHKvJfj78QiNrct/eUXIb/ABVH8RS+EUKhCW71YTtc2s8VzjQigajtimABIBz9RBbxQxC4uRkH8HH1f+lB5L+6RJJAik4UY2X3AVeWyxxgrF4YU4Gs+u/vxUF0qWMbmON3hlwNX5rb1ePBJKZIi3r7sG6E1c3HjiD1MaIwnxxUtwsiWyMpCxrg++rq/lmeQKxEbclPQCn/ALvw5E/HnOpv9C8qPD4o4IvGdklk3BI9Qe5qhufD1W9yNcWcbHJU91NXdoYCpVtcbbo45H6mV4VXErKAdsMalSXh8wmgbVC3Tp8K8l7+OeR1RtnXJHYrSXK8MvJ4nU+FIdakdM1e8atzEUgJd2GORGM1cr6BwcodmK4J97c6nnkuG8KHl1NQpFCNAZdXXufyLOuqGVe6EUwhSwjZUBBYE+/JwTU1nC00gTEYTLEAc8AbVHBBqtUEakaG1bd+/wB1cLhWNZ+p8TGT2A+stbN7RDdyFdoiUHXJG1JGCmp4m76815a8SeCzitI2w1ySz/8ATU7D7TW5515NeS1/x64xEPDt1P0sxGw9w7muF8L4fwOx8C2QRxqNTux3YjmzmuJ+X5HHQbNM2CPh0yR43dq8puEWnlRwGK7sCrSomu3PcdUojBIYEEHBFWtzPaXMNxC2HjcMtWNzFdQRSx50TIrjB5e6rVW8eWB8ATIV553HKrq0mtmVZMbjIx8+ygj0vcTfgo+n5zdqRhdyzz3GSsa50L9wAp0DmSaCMpGhXbVkjNPfpIUeODNyVALHfcdVFWvBJHOq4fQPzRzqLh1nF7MKn3tvQCjYKBTxROMNGrfEA1PwiylBwhRu61Pw65s3WUKJEU5z/MVPeCRXdHYGT8JG24+IqOzgjjVrpyrSewo5j9ZqhcQSSWdzvEWwf1T0YVc2728zRt05HuO/1F3LJJcys/PUR8AK4QxkM0LjVGVyRVgJOE8atHyfCaUAn9UnBBrjtqJYBKg3j5/CuDWvj3as3sx+sfj0FeWM7H0S0Q+1lyB9wrwvRbVyvt43Nb1ZuzwKW5/kSSRI1LMwA7mridDDaxKfVMe/3ZH7xUGia6vHJODGowegPP8A2qCTwntnDZULoPwJ5/ZmrZkDzrsD4hJH1YxneuKPHNbQzROCisVx78UJm8NkO4P7q8rZzNx24HSJUjX7F/ma8h+EWvFeNeHdetFFE0pT8/BAAq1aAiQWtslu8Sloyg0jbowGNq8uvLQ3w+TrFisWB6Q3Vm/M+ArOedeQXHLu2vk4YZD6Ncv8TGwGcr8a8ueHWllxlTAW+ni8aRS2rDsxBwaI7V5G3DPwZVbfwZ3QfA4b+Na3mkQEgEnGfjXGJIiIUV9TpkN86GJ5pUjUbscCuISrqS3j/Bw7fFupq3uJLeTWuOWCDyI7GvGNzi3t7cJrYEgEnOP4CrGwitFB2aTq38q50xCqWYgAdTQuoTyJI7qpYfupJ4XbSHGrsdj9xrFZriPC+c9uMEblR/uK9NtncTTQM8wx19ViOpqWV5ZXkY7scml/vdiVP4WAZHvT+nzr3iAtXjUxltQPXGKTjNsfaV1qdeGXEhdbnQx57VZ/J9shCToSeZLDJqcW1zEUMi+4gjY1ERLbxlt9SAn35FW1pb2ylY00gnJrjgQ8UdmYZWNUHuHOneEqVZ1wffTW9qGz6SMdudLeWsahUyQOwpL5XkVAh3OMn8h3bvPd+EvJFO570yMB4skmW2wBgD4cqhSVA7a8BxpOd6e2kx4TOxyB9uPsNPJcB45NWokgdM5AqKVZY1deRH1QGTV1bSW/DUSTAYzZxnpiicgDA2rykBTjl+D1lz94BrgvFJ+F8Rt7qBtJVgG6gqeYIpLaSdPWeERSAFmiBzIp/wBga/tE8lQNXGLKPt6Ug/8AOsivJmWDg/k3fccS0jnu1uRBHr3EYIG9TcVXyo8nuNT39lCk9kiPDNGCPaPsb1ivIpCOEzN0N0f3KKh3miHL11riltLFcvIwGmRyVIPzrH6CC4uuqjRH/qaj5uE2Yt4RIw+kcfcO3mlkKaQoy7ch/E0zEuRK24ODKRlR7l6CkUBFMUrqhkCqAc+ryzvmisSl1dwZAeT+sHHTb+VQyyBWcK3hA4Kscsv9K2wCCCDWcVxiyEUgmQYRzuOx81nP4FzHJ0Bww7g86vYBBcyIPZzlfgdx83ANPbW7+1Ch+wVJwizfkpQ/qmpuCSAExSBvcdqltbiA/SRsvv6VwwY4bY77+jx/+IrNeUYZuN3QVST6n/iKjsZ3HrAKKTh8Q9pmb91LbQLyjWgqjkAPyG5EN7IresdRYZ66ulXBj9TEWkhs+1kHYisB0X1h6oxzqRlLKytjwhu1TzWxbVjBDLgg7AAY3FWCMlpEGyCVyR2z9XeeHfWyyJKpeKPUV69M0ugwkaRnHQV5bWbR38F0F9WeMBj+vHt5v7PuLen8ASF3zJaHwj30c1qZoGHgyEESAroP4w6ivK/yKueEPPe2oDWJcf6o9XQ1w7jV/wAOjuooZFMVxEySxsMqQRjPxFHi178l/JqyYt/FMjKBuze8+bydsWs+GWUJXD6PEcdi+9JCtxchBhFwSTjkAOtcVmidokicMqrzHzrs+FZWcPcGRvi3LzcNt/SLuNSPVHrN8B5rzixtp2i8LOMb5qPjcbSD+7btgZ1VecUt7R2hjj1N+NvgDNJxS1JHiWSY9wBrh93b3HiskCxaAMmpuNwRu4ii192zgHFQcciBCvBoXupzSujoroQVIyDV1ALi3kjPUbfGmBBII3HmvPpbSzm66TG3/by+pC6zpxnO1RgJEi4ACqB91RTRTqWiZWAOMiuNxaL4nHtqp/h+R7q0iuEYFRq0kK+Nxml4VfICPSAR7zS8OnxkaDn9Y0/CrhuXhj7TVjwzwnLTlXP4i8wPeM/WcHike4YrjSFIcHqDQCiVoxkhXJHTl3rjvCI+IWUlszDUfWifosg/gaNldJdG0MEhnD6DGAS2rtgV/Z5bXnDLu/N7YXkSyRIEPgSEEg+4Ub60LK3gzkjkTbS5H/415XTG78nr+3t7e6kmdUCoLeXo6nqtXVheWZUXVtLCW3USIUz8M+byW4Mb+8E8qf3eBgW7O3RaGADr5vvvVjCZra7dCA5UIM8gPnKMkCuKn++MnRFVR9g83AI9p5Pgvm45DGLdJAg1mQAt15GuCxRSTS60DYXIyM4Oa4hFJDdy6hzcsD3Bo38cqaZ7WM/rINLCgIIuGztBKzeIyqwIwRXCIIprvEi6lVCcVxu2ghMLxRhdWQQNhtXAXLQyoTsrAj7fNxOMR3sw7tq+/fzR+vwqcf4cyt+1t9Tw2Lxb6BegcE/Bd643eiKEQo3rSDf3LXB7vwLkIxwkmx9x6GvKGMHwJB71P1EjBUYltIAO/apb+WKLAAZ2x4R56x3NR3PFYnjEkGsOavL5reSONYtbOOWaXijrOkU1u0evkabiU5nkjitdek4zmn4hPFC8ktvowQACeeaXiF6yhlsWIO4OaPFQl14LxYGwLZ5Eirm98G4hhCBi/vq7uPRrd5dOSMbV8q3QjEjWRCfnZp+Irm3CLnxe55b4puIeHd+BKgVSMh81DxAzPIUi+iQHLk9qTiV1IuY7QsM9DUnE5YvR1e3w8pI0k8qZgqljyAyaHE7iTJhs2dc4zmreSWSPVJHoOeX1l5FO4UxMQQDyJHTbqKNtdFhhyBuD65251DbXEckfrHSGOQGPvxtUsFw02VbC/wCpu1Ja3GuJnLZV8+2T9ZZXJtp1k6cmHcVP4F2JZbZSJEOph1Ze9FlZBkj2d+4PuqC1tYeLWvEJIvpYlZdS7alZSuDUV5JMNUduWX3Mtek3A52Ux+BT+LUbyb/2Fx98X/8Adf2kWfEb+0sJYOGz+HbmZpW9VsBgvRSe1cI8lLy9KS3AaC3O+Ts7D9UGrOzhtoYoo4gkMWAE9x6nuaSHxpjEhwo3dugA61PxC1Fo0FtGUycfZ3+dAMzRD9cVxHe+uP8AqHzcCAFkx7yn/YVmuM3epjb6fZZWzn3Vwy89FmJ0atYC88VPfTC7lEmJEEjDQ24xU8lhImYoHR/jlasrOWe1utI6DT72FWdy1lcaynQqy8jXEL/0wphNKrn7zXB7Z4LclxhnOce4ebjYxe/9g81p/wChvx7o/wDy+pjlkibVG5Vu4qSWSVtUjlm7nzS3VxKoWSVmHYn6ggMCCMg1OVtOIo8uTGc6eoAPar26dpAba5dix9lQQBU8dxLxGMRuA0aLu3cDNQBp7tjcyevFuFxjlVtJC7SNJcPGSdtI51fyRNaQIsrMCxOo8zirV7VJYlF5IxyAFIODUUCXst4Qe+k9jmrAyy38YlU5iUjf3VxpiYI0HNn/ANq9C4jLCsMk0YiwAQBvgUIo14nDGPZhT/YZq8d76RvBjysSk6u9R3UbcJk0gKVXSQPfVqsCxLqvJUbmVXOKu7iD5QgZ29VApz++vlGxlSQeJlQvrbHkdqlFtCjNbXkgPRcGrFpntYjL7RH/ABvC5oIroGUkAjAbsTV5wx0keWJlcZ1BOuKQghgVJPMiozJGS8TlCKXi1+V5g45nFDi143JQdu1Pf30oIaUqunO221FAGO4LEAgtyINIJrhjHEPVX8c8lFNFb2PD3R5A7Sjp1+Hz4m0yIezA1xRdN/P72z94z5uAvm2lXtJn7x5pLS1kYs8Ks3civRLNZVU26Ln2Wx17Vpsw0mbcGbJyuM5z1+Br0e1YI4sVGpgN261HPocobdlRQN13AJ+FSrZXIeR4lKjYP1arextogrC3VW+8jz8YfVfSe4Aea39Xh163do1/fn5813DC8aOTlzt55JFjQs3IUjrIgZeR87Wc626zlfUbl8+SKOVdMiBh76itbeI5SJQa0KDnSM960JnOkZ74rwYf8NPuFGKIgAou3uoRRA5CKD8KVEXOlQPgKCKCSFGT1oqrYyoPmKISSVGTSqqjAUCvCiwRoXf3V4MX+Gv3UYoicmNSfhQiiGcRr91CGIHIjX7v+PWaVXVw7Bl5HPKpbOC/RJYrhNY9s43PvNGwuNLCF0mXfdSM1E2gPG0bZ3BFRF49WEYmoY57jUIos4BBOcYDVDwvxfVa7QMvQetgVxGWCOGK2gl1BfbxsDWScb/UcS9dreb/ABIVJ+I2Pm4HOEuWjJ2df3jzYp1RlKsMg0bWVN498EkHk2/fvSJJv4niqxbVpRMgH99Ilw2pCGKE5JPqas9+tR26o+tgC3QDZR8B382KYhVLE7AZNXEpmmkkP4zE+Z/o+Fwr1llLfYox894YpGVnQEqdifOyqylWGQaVVUAKMAeczzGJYi50A5C/lhWZTlSRVvOYJkkAyVNHjKaHK2wWQqQHq34vdRyhpHLp1XarjiokheKO3VFYYOKBI5H5ioSKIIOD80fT8MI/GgfP/a/mjkaORXU7qQRVvcRzwpKvUbjsavHlR5pPpMrp8PB2HxrLArOHbX6SU05205xjFWzOGtX1sWlRi+SSOWeVWwnIuQJAzCXALfAU6k3Q0u7OHy250qvarbVm0k1tmZW15ORyzy91DxzDdqJCz+LpBJ08wKs8jxEIIKkZy5cb9ia4zdCKDwh7b8/cvmRGd1VRkkgCuJsBMkKn1YUCfb1+cFYkAAkmiCCQRg/lzhFos9wS4BRFyc9zXGLSFEimgUBTsce/cGk9pfjXGbeGEQeGirktnArhthFKrTz/AINeQ74pbzg7yCL0YBScBtIrililrKpjOUbkO1WcdonDRNLbq5GSTjc71Dc8IlkWM22nUcZ0iuKWcdtMvh+w4yB2xVpAZ7iOPu2/wq/sLZrWVoo1V06AdqEmBiicn5vD50iuAJPwbgo/wNXVu1vO8bdDse46HzcMv/RpdL7xtz9x70YreVhKFBzgg52OOVC3h8TxNHrZz9vfFJbQoxZUwa8GLDjT7Ryd6Frbhy4Qhi2r2jzpLeFGLKmDv1O2e1GCIq6lAQxyw99TTW1lCzFeZ2Gclj9tXE8k8rSOdz5uHqIhJduPViHq+9zypmLMWJyScn5ttPCtmELesRLsSNJ2GM/wq/cyvEI3BGRpw4O+O3Sr54vCRHYSXAPrOvIDsT1NLLZmIJIy4IiPvyibj+FNPZu82p1BnwNgCFwv7t6R4NURM6iMGLSmR0xnIrx7Ux4JUMtvgHvnp8RV5KjX8b6wY/FyPXDADP7qaaOfxl8QA+IhBduik5wfto3oJJ8X1PSs4/U50ksEAcNIpJMrAoehxjB71NMhhmEci7ux2cLkFRuR1/KdrbyQ8LLRoTK4yAPfyq1t5peHSW8yFSMhc/eKAKyAEbhq47jTb47tWccDwv5v/wC3mfWG9fOffVkkLcJHjMRHvn76t7LhuPGhDyaDkAHqK4jeG6mHqlVXYA864Hb7Szn/AErXD/TBcXHjQsFk9bfvV7AYLmSPoDt8D89f79ahf+fCu3d0/mKghaaaOIHBZsUkVjNN6NGjA4IEpbmR7u1WHE5bQ6SNcfbt8KgvLe4XMT593UfNu+K29vkKQ79hReS+nJmuETbYtsPgK4hblLa0b1ThSjMu455FQQSTyrGgySavpo/Ut4T9HH1/Obqf8h2sSyzxoxAUtuT2riPEmhkRLaQYC7nY1ZcVne4RZ3BQ7cgK4ika3hZGBVyG2NcbkRxBpdWwW5GuG30Iha1nICNnBPv6UnCrKNxK10rIDnGRXFr1LmRVj9hOvcmo5IxwVl1rqwds++uG3htbgEn1G2auLRRGQTRup1bMARz71PcJZWESQyKZNgcEH3ml4xehly4IzuMCuMeDKkU0bgnke+D8+KV4pFdDhlOQaYeOReWu0qHMkY79x7quJ4pdJS3EbZyxBJzXh21tbwtNEZHlGoDVgKtXUHgTx+CWAdFdO41dKHEOJWzaJCSezihx6frClPx25I9WNBU91xCaLW7OIycbbKas7SG4imLTFHTcDG2K4hav4EVxpXOArleRxyYVbvcsGgiyRLgFalkSziaCJgZWGJXHT9Uf5E4lfXdoI/R7B7jVnOlsaa+XOL/oGb9v+lfLnF/0FN+3/Svlzi/6Bm/b/pXy5xf9Azft/wBK+W+L/oGb9v8ApXy3xf8AQU37f9K+XOL/AKBm/b/pXy5xf9Azft/0r5c4v+gZv2/6V8ucX/QM37f9K+XOL/oGb9v+lfLnF/0FN+3/AEqx4pxG4uEjm4VJChzly2QPqIpZIXDoxDCmW3vt10xTnmvJXPu7GmmMPhxXdrqaMYTJK7dveKgla74lE7/ng46ALUJRriG5bGXjwvuAySa4ewlvZ2OndHYZGwNX0kTQRLrR5QTlkGBjtULwJY2yzyARuj5XBJOW2I+FBjZ3eY3Vwp5g7MDUNvcXGsp9HBqySxwgqS6ht0aK0zk7PMdifh2H+Ro0Mjqi82IAr0H6Z08TKhAwbHMEgULMs9witkxnA9/raa9CuAcFRyJzqGBjY5NS2Do+lWBOSMnAGwB7++o7V2meNzo0AlzzwBXopdvoXDrgbn1cE9DmvRZ840b6SfsBxRsrgNgqOvUYGnnmhZN4bsxwVVj0Ps4/nS2TvAkikEsW22GAvMkmntJ0VmZQFUgZyOu+31cXEJVQRyqJY+z9PgaEfDpjlJmgbswyv30tlej8DOkg0lRpccj8aisuJwOWSBslSvQ7Ghwu/P8AyCPiQKNiQF9IvIkCjAGrUR8AKEvDoPwcbTP+c+y/dVxdz3HttsOSjYD/ACPDM0Lh1AyAcZ6UL+bbVhjjGT2yG/hSXkiSSOAMuwJ+xtVC9k0lSilTqyDn8Yg18oy6idC755ZGM4/lXpcnjvLhcvkMOhBoXh3Hgx6dvVwea8jXp0hByqliCNW+cMc16bL62VUhmcsO+uvTX0MgRACGG3ZsfyqO7dFVdKlQGBB6hqlu3lj8MqoUMCAOmBjH1wlkHJ2H20Xc82J/yTYyRok5diNl3GM8+maeG3klkYhMF9zqAwmNmHxp4bRxEZCqjTEA4bntuCK8KFElHhoJDETp1ZxhuhqeGDMrAK3rtqbWAVwdsVewwo8fh4UNnbOSPjua4iiGFGVlGg6cbZI7jHSoUg9E8JpE1yKWHxHs71DBbJIjkIVLR6ct3U5/fQt7bQCyqNt217htWNOKaKzKsFQA4kwdXLQdvvpoLWI4VELFJFwW22AwedG3tXIJKn2Q5L40jQNxU8VsIHKABlEZznnqG/8A9bf/xABHEQACAQMCAwQFCQUFBgcAAAABAgMABBESIQUxQRMiUXEQFDAyYQYgI0JSVIGRklBgobHBFTRDctEHJDNAU2IWRYKQoLLh/9oACAEDAQE/AP8A38gCSABk12EvVaaN095SP+RJAGTQmiLBQ658M0zKoJY4ApZY3911Pkf3NSLbLA/BRzqKEBtSnPd3Xr3hilR3VCC6gsM4+NSIWR0wRgjc12SZ05OcZ1DlRUrzHtWYKpJ5AUeJFn7kTFQdzipRNcppCaVPVudeoQrpIYqw609rrGl53IPSmsFVkaHYqc4JqS5lRcdgdfTqKtr1JzpwVfw/cpApcajgU0ZVg2R3hgkYoAYYDnp2/wDTg4/hRDMq6VyDvmiuGGc5xjHhq/rQUMmAfeUfHrVyiqiDUMjlj2k86QoWb8BUdzJcLpRMHqTyFQxrCgRayxYYog5zRGeorDClY9aeJhIZove5FT1r+0O/p7IjwztvQOQDj2j3cCHGrUfBRmhcTv7lsQPFjii190SL8zWu+HOKM+Rr1p1/4kDj4jcVHPFJ7rg/D2pzg4qwv2uZJY3QKy9B6biYQQySH6oqwuZLmHtHQLuQMfsa1dzG4PgFB86i6v4/12/pRbcjbJBzzG9BQylQoAzkUcrHIPgcU7M7Ek7+zZgoJJwBVwI7kxohBOc6vAUdlwBSIzsAAST0HWrbg5IDTtj/ALVpLCzQbQJ5kZ/nXq1sdjDH+kVLwq0fkmg+K7Vd8Pmt8t7yfaHTzrfNXkHaICOanPmKjliIUKw3Gw9lLcBDoUF3+yK9Xkl3mfb7C7Cu2gh1LHGSV56RyrUXjDRkbjIJq2eZ9RdxsxXAHhUcjtNMpOykYpbiRmfEWpQxGQd6lhgcjWACeR5GsXEHImRPD6wqOVJFyp9lezXMDpIu8Y94VDNHPGHQ7VcEWfF1k5LJz/HY1xfiEluEji2Zhkt4VY8VukmVZHLoxwc1xqYlYoE5scmraHsoY4wOSgVYcAsrKwkvuMZGpSI4eTbj/wC1Np1HTy/Ylk65dDzI286Uc1plySfgf9a0kK23jU7hInO2+w9pf6+wIA2z3vKreKKGNSincDJoDWRgEknA+NWFitugZsGUjc+HwHovb62sou0mfA6DqfKppzJJPPLOwmDnGDjHgBXDbr1m0icsC4UCT4NjcGiAeYriViIG7SMfRk7j7Jo6sjfarqIRTRPEO8W5UOQ9hJK7uYouf1m6LRVbaFmVCxG58TUEpZt21EjoO6tSQFrhwHZVkTfHiKgWRU0uBtsCKii7PtN/eYmkiKNKwbdzmoLZI1UkDWOZpfpbtm+rEMD/ADGhdO0r6FDIuxHU/EU8WrEsR0v/AD86hmEgIIww95fYyPEoxIygHxNSI9lKJYTqiauKtFc2aTpuUbBHUZp7ZuJWcEqH6VBpYHrirPg84lV5wFVTnnnOKtib7i6lQWGrZfLlXCOC2vBrY8S4njtFGUj+yf6tXF73iXFJTdSQyCAe4Ap0KP2LGcSIfBhSl2uWBYjukeW2ajuHVFz3i2ACTyyTTSylZmLHmMfhV3IXMfhpz7SWdZ27BQffAY/AUTvgMPKuD2weVpm5R7DzPo4nxa34fHl+9IfdQczV5d3N/ca5SWY7Ko6fACrX5Pf7gRO3+8Fe62AdHgK4XeT8K4i8NxkIzaZP6NQOQCDkVLGkkbIw2YYNTxtFIyNzQkVPgIkg+owNQzxzAlM7H588jZEUfvt18B40w7BI448BnbGo/wA6U6dKSPlmz0pbdkDBpMRAkgDb8zU3EkTaJdR8elPeXEnOQjy2olj9Y0ski8nYeRqPiFyhGWDD41Fdw3ClM6WIqKAqVVlBC+642PkaaeR3IhUEL7xPI/AU4MirPF7+PzHhUUqyoGHsLiR3nkZueoiuFsXaWFhlCucVfW0lqXVSdDjY/wBK4JcmOYxOdn5edcWuextWA959hX+y+ytkHE+L3QULAFRHboebUOIHj/ygtY5drYOdEfwAzv8AE1gY0hQBjGK+UtrBa8XnjhUBCFbSOQLD9iKrMcAEmooyJJXYbhtqk1JFCvUMd6dS6zLp3JyKlDFYzvjT7M1ZK8c0qOveI1ZrSM5FcJQJZJ4sSx/E1x28ltbItFs7sFDeGamSQaTLKZQ5AYNvz6iuAcDFufWZxl/8MeA8fR8oLCGWBrrT9JEP1DwNcCuJp7I9pjuPoUgYyoHo4umLsn7SA/0ogIpOOlWCSAyMVwrYK/Od1RGY8gKtkOGlf3n38h0FSxLKuk+YI6GtAi+lllLaRsTtirq7ec45J0HoALEADJrsJBzAHmQKaGRRkqceI3HptL3lHKcg7BjXq8qqUjkCofhuKRFRFUcgKP0Fxn6khwfg3zru+Fs6KULZBJ35UvF7Y+8ripl4fcOXW40E89qtPUbdSEnQk8yWGTU629xEUMi/A5Gxp9UUzDO6scEfCri6uLhg0j5IGBXBbi7/APD0NnFE/ZvO80hAPeb3R+AAq1teKRzRzQW0+tGDKVRjgioON/KF4cf2G/a498kov5GpPkx8oL+eSe4VFd2yxZx/Jc1dfI64tLGe5ku0JjTVoVSc/if2HAFjhLnmaVhsirt8d6co2ARnByMUJR76gClWLDry2JqRCjlTzHs4Zklu2KZICYzQGCa4cc2UH+Wr61S6tpInXII286eXsmIAcuhIAbkpFfJri5OLOd9/8In+Xo4osl5xKCwaZo4TEXbH1jnlSWZ4VxGyS3ndknYh0Y55dazXGCPWUHhGP50+yP5GrOaOSJVU7qACPnXH0kkUPQnU3kPTf3Blk0Ke6p/M+iNA2SThRzNKoCAxjYjZBsT5+NMSWIeNSwQknGN6BchSq4QjmNtJqWOMlQWHaEbEbK1YIJBFYrh9z2iaGPeX+I9FxH2sTL1xt51byGSFGPPkfMfOa3gb3okP4VJwy1bkpQ/A1LwhxvHIG+B2qa2mi9+Mj49KbOo7dfR8h5oIPkdwx5ZURQJMsxx/iNV78sOFQEiEvO3/AGjC/mauvltxGTIghiiHj77VPx7jE+dd9N5KdI/JakmlkOXkZj8ST+w1GuBSNhgDbpiowe9l87eGDRBVjsdzSDAIP1zypEl5Zzsc7VcsGmcjxx7O3120zKyHS74DVvr5muCyhoHiJ3Rsjyb0fKSz9X4gZAO7N3vx60iygdogI0EHUOlcF47HerHBKcXAX8GxVzZQXDRM6nVGwKsNiK9Tg9a9ZK5kC6QfAUa4hMJbmZumdI8hTuY4yxBJ6CrKN1EjOpBZvnQd+4nk8CEH4ei8l7KB2HPkPRb2AmiV9eM/Cm4awQ/TbDfGKt7KWcCR3wOnjtTWc+DouGzV3BNFoDSl9RqPhsjqpkkx4DnipeGOclZcn40yMjFWGCKgkMUyOOh3oEEAj0Qdy4uI+mQ4/H2LY0nPKn3kbHU1NDLAwWRSpIzvXB53ksUQuSsbMFBOwzv+x4ZmiYEE4yCR40by2b/DP5UbqLl3v0ilvIeur8hVxdB1AjBUfWPLPtL91WHfOcjT5igSUVj1WrK6a3nWQZxyYeINdtGYu11qExnUTtivlLLDdQwCC4hcq5JGta7CcKyiRADzHaL/AK1wVOw4lbySyRKik5btF8KhngmBMUqOBz0kH0cTuxBCUU/SONvgPGuox0q4lEcsCsCVzk/OJwKsh9AG+0SfzPo4o/8Aw08z6OGSOZShY6QhIH41xF3SJNLEZarV0kgTSeSgGhasjao5nHwJyKJke7jWRANIJBHI1xCV4oMocEsBmuGzyyCQOxOMYzXFFAeNvEEeizfXbRn4Y/L0N3b2I/ajI/Lf2N/J2dnO3XQQPM7Vwaz7WUzOuyHbzri9p29sWAy6biuAOcTRn4N7ByAjEnAA50bh1TGMk40H7Q8TSSXiMAyagTU1wY3VQmSaF0wdVkiK5o3UmtlSLVg+NG5lVGZ4sYIxvXrNwQCLcmjeYmCMmBtk1LcaJY0C5LVNL2UZbGa9blChjB3fHNNdD6PSuddG50zdm64HRqjujIz6U7i82NLdTMMrBn8aa7dRGGiwzHlmiQASelC7lbdICRUTu65dNJ8PaQPGpIceHShNDg90dOgp5o2VttyBjYUksQjwR3vIU00elwoG6/ZA9pcQiaJl69Kh7WDQkpBUjAPga3BqaSWSzltlbuvg79CDmpLcRnDyYPkaEUX/AF0/Jv8AShDH94T8m/0r5MT2tvLPG9ymqTToG4zjPjV3xOCHKoQ7+A5DzNTTPK7MzZZutPIETUeZ2UeJqO1mM4klYHA+dLtG/katP7tF/lHo4p/eF/yCsVw630gS55gjFXtv28WNWMb1FbR9gmjusVHeFRLcq3fkVl8t6uLiOKaEH45+ANXEK3EWnV4EGrS19XDZbJNcQmWSUBTkL6OG/wB2H+Y+if8AvNr5t/L2MkaSLpdQw8DUccca6UUKPAeiO3giYlI1U+IHsCAQQRUmILkF8lTy+FTykvmOVjk8hUiyPdKFbdVG5qPMkx7Vt06eVRtGxYtKyn4VOyGCNQ5IydzUJgDoBO5OdhUcYnaY/lVvre5QPzQfyq+bEajxNdhdOgRnULQVRdxoOSD+W9TOblm7Ncqg5+NLKhs3xgEDBqLsgozO6nwFTSR+sxljsAK9at3VhqyMb7U/YoCY52B8KtmdoUL8/wDnbxJHhITnzxVteKyKrqVIGCemaNOqONLqGFHh9rn3SM/Gv7Pth4/nSWttGQRGM5rO1OyRDU3M9OpNLJLcXSlVKhPH57jKsPEVZnNtF5ejii4ljbxX0JcTooVZCBQnuGjLdqxx7w+FE3JCYlIj2w2cV2k4LKbo7DOwp4i6hhKCzHrtUZuoSqK5BO5Xwqa5mcsvakj8s+mwXFsnxyfRLvd248A5+fNdQwuiuTluXpsrK4vrmO3gUF3O2TgbDNXlpPZ3MlvMuJEOCM59IuYmmMQPeHz2RXGGUEUkMSHKoBWlc5wM1pXOdIrs4/sL+VaE+yKCINwooKo5ACtK5zgZoqp5gH0aF+yKCgcgBWhPsiuzT7Aooh5qK0J9kVoT7I/58ohBBUYPOluZbZ2R4W0n3aF1HkdorRn4jam72GDDFNpOMsKkkjixrfGeQqS8KYIgYg9eVWiyu7yypjPu+xtO6JY/syH8jv6OJRloQw5qfSpZSGBxQuEfZ9s8x0//ACmdfqFCMYyzbkUXhADZGoDAA72PKnmZl0jIHieZ9GaAJIA5k1EgSNF8AB6F71456IgH57/PeGKQqXQEqdvTBPNbypLDIyOpyrKcEVNNLPK8srs7scsx3J9IijDlwg1Ebn9sEA8xU0YljZCedLw9gwzMSgPu1NYwuhCqFboaisdMiu8rMR83Pzj9Hdg9JF/ivodQ6lTyIxU0TRSsh6VbJGyIvc3zryN60oSYdI0dkGz1z45qZV0zroAEbDTgVOY/oSUwpTpSECA6kAQrhfEnxqbBFwmkYjI042NfRdrbNoAXs8451dYOhgQQRt3QvKuHQa5O0Pury8/QxCgk8hVoCUaQ83Yt85mVVLMQABkmlZWAZSCCMgj9uX87RQ904ZjgVYTys0kcpOobjNNyNcOmkk7XWxOMVeXToRHF75owcRVS/bZPPTmrK5aeM6xhhVy9w172aSlQcVJBfohYT5wM4qxuHmiOv3gcGp5RFE7+Aq0upxMgkYlW8axv866jLx933lOpfMVDIJY1Yei9te3TK7OOVCSZFMeSKM0ujRq2pp5WUKWrtX7u/ujAo3ExQLq2xjkKaaRl0lqEsgKkNuowKjjmuZAM/wCgFRRrEgReQ9F0S5WFeb8/gtAAAAfNnhla5Lhe6NG+Dnn0q1CxxymVCMAlsoeX9a4XDOtxJJCjRWbDuxPzJ+0o+qKaO7EmtFbIMg+GGaliulWHCMRDk7nBJLfx2pkmxIOxbWVk1Ng/hg12NyHyAxVpskeGOtW6OLOVdBDmP7JBzihFJAIW0EjQwIRepAoWrAAaO96tjP8A300c02ghGAAjUhh1Gc1DFIJYi6NsoG6k4Oo/tOeVJL1VZgEQ7k1NLGl4ksbgg88USChPwrhefpvwr/zTfx/p6BpxtjFXLSjiH0a5bbH5VLc3meyk0pq61aW4hjxnJO5NcSmHci8Tk1eer9jF2cikpttVvL2sKP4jf55/3ebP+G53+DVJII42c8gKL3KJ2zMMbZTHQ1c2aTjI2bxqW3lhOHX8enzYLGWUgnKr4mgq20QEcTN4451ay6pZhuMkEA1JIsaFmOwq3RstK47z/wAB4fuHM5SNmAyQNqtLNZEZpkOS21XNhEsLGJMMKtGc2wVwQyjG9cNRl7bUpHLnV5bSGRZ4t2HMU19cspQW7Bj1qxtnhRi53bp4U6v/AGkp0nTtv+FXluJ4iB7w3WrB5BGY3Vhp5Eikha4u5GkQ6KPD7XBwm/nXD+0QvG6kDmPnuiupVhkGh9HmCbdG2Vv6Goo3TIaUsMbZFa5pZZFR9CocZxnJqCTtY21gZVip8DijaWcw1LjzU0eFxdHal4ZCObsaigtY30qF1geZq4nkiePEepTsfHNWsy9o8WT4rnn5VIIhiR9tPWkVp3EjjCDdF/qf3EtoIZdXaTiPHLIzmvUbP7+n6a9StPv6fpr1Kz+/J+mvUrP7+n6a9StPv6fpr1Kz+/J+mvUrT7+n6a9Ss/v6fpr1K0+/p+mvUrP7+n6a9StPv6fpr1K0+/J+mp7a2jjLJdK7fZA9g6K6lWGQaBlttjl4/HqtKgk1PBNgP722adBBasq+H8TTgiJ4RyDZP8gKugUt4wM7Mo2q3VxI50sqYGAx606yNczNGuWVlwc/DlRHbw4ZSuR16GpJYotOe9JjAAG5pYZJWDzfgnQef7jMwVSTyAr1juK2ncsQRRnAWMkbMMn4bZrt48cz+RpLhWXURimlARWUaskAUJcDvrpOfOu1j8eoFdtHjOT06eNduNQAGckD86M4EjKRyA3+JpZUYgA7n2b2qE6kJRvFaL3cYw0ayjxGxo3Nuf8AiROm4O69R5U9zZyKAZRjINeu2v8A1AaFyMnsoHYnmcYFaLuX3nEa+C7mooI4vdG/Unn+48iB10nlXq0fTIGc4/DFNCrKqknCjH8MV2C7YJBGMHyoWygAajXZLoCZO3I12HLvtnffzr1dcjBIAIOPKuwXbc5AAH4V2IyDk5BB/KmhViTkgnH8KWJVbVk5x7Yoh5qKCqOQH7k3CsxjCgHc8+XKlaREUb8vDmc8qV5l1aQScucYrU5K946Q3PHPakeTYEkbDAxzqF3IbVk4q3Zg7AgnO+fD4U7SdtrCnSpA/wBaeSVlK5IOGzt8aMkuTgk+Ax0xzoPMCCWJ93bHjQeVubEAEHlQeQePXG3PekaTWMnYlunh/wDG3//EAE8QAAEDAgIFBwcICAMHBAMAAAECAwQAEQUSEyExQVEQFCIyYXGRFSAjQlJTgTAzNEBicqGxFiRDYIKSwdFUc6I1UGODwuHwJUVwhAbA8f/aAAgBAQABPwL/APQfVrSgXUa52n1UKNc5PuV1zpNuqqgQQCP9xOPNN61rA76VikJP7W/dUfEI8hZQi97ckmW1GSkr3mk4rDP7S3eKbkMudRxJ+P8A8NLebRtV8N9IcStN0mpKrOMd5okW16uxHSvWRjR585txvWYWO08b6jUX5sjgo0taUC6jakOtr6qgfrpUBtpqZHdcUhDgJFEgDbWMONOPpKFhVk7qawmWsA9EA9tJblxJRyNlRTwBtXPsW/wx/kNSVzpK0aRlQtqHRO+l4NLHVKT+FQ7NzmtIQnKrWaSpJFwQRT8llgAuLtc0laVi6SCP/hZ1zalGtX5U3oWwbg5k7b7aW3ndcKTr1b9taRQLmcKVlAtu206W79HXcX22ArTN6HJ6+kvlptSOkpeq2zXcU2peot2SFNgm+6mRd26yTq6N9VO5M3Q+cGvV/WkvJJANweB+ty5GgYU5lvapEx+SemrV7I2UliWyppaW1Anq6qGHT5WuQ7lHD/tTWEQ0bQVd9DKlPACji8HNbOfvW1U/LYYbC1q1HZ20xiMd5zJ0kq3BQtetK3pQ3mGe17U9hsR25KLHiKXhcpg5orx7tlOtz5LpztqKkimX34y+iSOIqBM500VZLEGx4f8Awo4vInt3CmyG13W8AOFKsXx0woKGru4Uq13ipF/zFqaupT+QqPRGo7avltcADZ8RQzgZ9DqtbNvrrJJHV8L09bnAABslOsCtjoXqzKRu6RpgLC3LWTs62unM6nwDtGu3dSVBQuPrKHW3BdCge6sRnMNtra6yiNlYREdCy6tvo21Xp55phGdw2FTHy3DddbOvLcVh81xfoZHzlrg+0KnBRiPhO3JTDsHyWgqylATrT21LU3zjDnlizXbuqc406/CQ2QXNJfVuFMHSYvKX7CAmormaZPfJ6COj4VhuJGQJJdsAjWO6mHm32kuo2GsXjLdbSW2wSDr41hMxkNhg9FV/GlKShJUo2FaRFgcw17PrinW09ZaR3mjOiD9sjxryjC9+KGIQz+2TQkx1bHUeNX+ukhIJOyudxybaVPj55ISCSdVCVHJsHU37/wBy32i4kWVZQNwaVm1ZkhIzaz3U5dZB1H0ez40coSTrCbHWP60bB1tSnLpUOsNVOXjuHL0mzxrnbRPUXs40jNJfuu4bGuvR6J1QvZSrAcaUlQUgAZLqOobe+srVnMic2u1+FDTaki+bd/emkZEAXvx+sYniOa7LR1esaYVJb6TOYX1aqg4WEWdf1r224VJnuc45rHRd3idgrSvFxUKYE+kT0FjZQeX5OlRV/ONdHvFJwlTjDSy+vTADKT6tICghOc3NtZo4fh2kzlpF6WqMtORZQRwNqYjw2SSyhAPZT2HBbqnWnltLVty76egONQebx9edXTUeFTm1NS+bNftm0J8KccfL4hRCEBtAzL4VEkSEylxZBCjlzJWKm4a3IutHRc/OpC5pTkez2bqPI1Bpw9DcfZpkENoBVfVt+rkgDWaexWK3qBznsrylNf1Ms/1rmeKP/OPZey/9qGBj13j4UMFijeo15IicFeNHB4n2vGlYGydjiq8kSm9bT/8AStNi0frpzDx/KmsaRsdbKe0U0+y6LoWD9aUMwI4062W3VI9k1Gd0rLa+I1+diz2RjINqz+FYU3nkZvYH7mPNLvnbAzdtJR6a61m4V1u6tjRUbgn1hrvenQFk36qRqIG016doKTYLARr+zQtnvzc5dH8e+lqecQhOWw/OmlWS42LbLgml2LaF21f6lU1m0ygDY21Dd3GmWsgJIFztt9YUMwIO+pcbm8ktg5hu4002200lKU5QBUial9s81kpDiTs406oTmQ+10ZLO0f0pvT4g9HdLejab169pNOGKwVPLypJ2njSp77n0dqw9tf8Aaih9fzslZ7E9EVzRj2b95vXNmPdJrmsf3YoNKR82+4n43H40mZLa+cQHE8Uaj4Uy/GkEKTYqHHaKcZkx5Tr7DYcDu1N7WNSJq2GEZ2xzlepKRTTwgNNtuqUt1xV8vC9KSlaSFC4NOMfrSmkC3TsL0w1oWkN3vlH1UqAFzUjFkDosDOr8KEPEJhu8vKn/AM3UxhcVr1cx4mgANnJImsRyA4dZo4zH3IWfhUWVzhsqyFOvfUqa3GLYUknNwoGlPtJVlUsA1cGnYsd3rtg07g6knPGdIPA03iEqMrJKQSOO+mJLL6boVf6q4sISVGmJYcOVWo7uXF2srqHPaGv4VhD3RW18RV6l4oG1FDYud53UMVl39U9lqiTUSRwUNo5MSd0kkjcnVWFs5I196zfkvanMVQHwkC6PWNAggEfuQs5Uk9lDUjUogqFtY1HNvonKtCQMp1kjjakdLeom/SvuoAFBNzkLnU3qpWbSqJVrA3erR3jt1cPhRIzJJ3EbdgpCsoN9i/W/oKaSUPtC3/8APrEmQiO0XFUrF42gUpJ6e5JrCYxWTLd1kno/3qbLcjFCtDma9c8KfjR21c6QgORl9YezUXDY7TwkNLXYp2d9SJtlFlgZl7+CaSx0tI4rSOcT/T5BxpC9exQ2KG2m5y2iEydm5z+9PR2wpUpDeZ0I6NYSyh0rlOLzvXsR7HJikLTI0qPnE/jUTE2VR7urCVJ1HtqNKakAlG4/U5c1qMnpHXuTVpuJG56DX4VGgsRx0U9L2jt5JeIaBzRpbKlHZTq8XyF3qAbqgSVSI4UrbexpTTSyCpCSe2mLIxhxNuPJi+uTFT/5t5JCW5WKKQtVkjVfuoYZIaILMk2oU3JZcWtCV3UnaKcbQ4nKtIIp/C3WVaSKs91RcVBOjf6K+P1RaErSUnZTzCmldm41Fk5ugvbuPHkxFrSRl/Z11Dd0MhCt2w9xqU7o47quzliOFuQ2RxqQ9oWVr4Ck5nHAN6jSEhKUp4Cr1OxDSXbbPR3njUGBpbOODobhxoC37kOJzIUniKBPQSdeo6js4UpN82q4FhY7RQPSRdShr37qSvU3Y9Muaqv09Wy9s++/9qWegrvPR/qKGtQ1kjVu4a6vZNz6358O6mNIp1KSdQOb6xjEnO8GhsR+dRcKU+0hwrsCdnZSUBICRsFFIIsaYw9Md5akLOjV+z3XqVLWpZYZOv118OzvptCW05UjzXFvyX9C1T0aXCsvNq4imXtK0lfHlKQRYjVTDqoaglWtg7D7H/akxWhIL6dSiNdthqbiTEUa+kv2RUKa+p7RSUhJWMzfdwqbhS87rjVstr2rDZOgkp19FWo/Up2JJZ9G30nPyqLhinDppWsn1f710Up4AU9inT0cZGkVxoXsKxlBAZeG42p5/EZEcqDdm+zfWFyIymQ0jUobQd/IsZcbHbb8uTENeIxx3fnTjgQhSjuF6gQ0TA847frVDhGMpfpVKSRqB3VMeDEda9+7vrB2MrSnTtWaffQw2Vq2CmZDT6Mzar1Lw9qSL7F+1TEt+E5oZHV3GkqCgCDcfU3EJWkpNPMraXbwNRpV+g5t3GiAQQd9Oo0bi0eybUyedQMu+1qKSkkHaOSC0XZCNWoazWLvdRod5rCmc8nN7AvRISLmp04vXQjqfnUCDpfSOdTcONDV+5UpAZWV2ulW7tr9nc22jvokhahrTrBANH9p0r9Ia+Nev27L7h9mj1SCQOnbLw7qSvrHMOHDVvq/qkd/3eFQ2yEZ1bTs7vrGJQSwrSZrpUr41CcLkVpRRl1bKleUG3i8yQtG9r+1InOzJDKGcyAnpO3/ACqfJU2A23845s7BxpptLSMo8ePmyJmU5Wz3moj4iTSpXVP9axLEGHWNG2b3qGoICGTttfx8w2IIOyoL5bXzZw9rZ7OFcyjXdOjF3OtROHxdE287nU0ej2UH21s6VHTFt1IZclPK0Tdrm/dTSVJbQFKuQNv1DEZ+i9E184fwqBh2j9K7rcP4cmMpd0aVhRyDrCmp0ZlpCYzV3FDZULnWRRkEXJ1dlTWtNGdR2aqwnSc1yrQRY6r8KVhccv6UZknsNuSyb3sL1mFajSkJWkpULg0yy0ynKhNhyYmVvSWYyf8Ay9IQG0JQNgFT5aZEgIv6JJ/8NLhZbPwV/DjUV11xlKnEZVcKkRm5DeVY7jwpl17DntE7rbO+kqCgCDqP1G9GUwPXFHRPote9OtLbXlNRZOxDh7jWKt5ZOb2hWFP5HS2di/zqTAZkazqVxFJwYX1vau6m2WY7ZyiwG2n3C66tZ3msLAbjrdVqufyqZOW+cqdSPzqDC0xzr6g/GlPMtWClpTTchlzqrB/cqQAplfdTDAzFajmN9XZTqEGT0gNaB+dOw28wCSU91J0qlABFh1b21a99RYzYSrOkE5jrNMMNuIcQexQ7L02yVLCFa/SHX3fWcVJelMxx/wCXp5zmzAyNKXl1WHCvK8MtLVnsUpvlOo1CLgihx+2ZQzE23U0C64uQravq9ifMOqpM0q6CNnHkZBdIbyZv6U9GEcBaRm7Tuq6s2a+vjUd7TN337/MebKkXT10m6e+mH9OwlxO8eBrDjDbZdLxQHcx0mbbWEEKVMU2PQlzoVG/VcVW36q9lD5fEJvNm7J66tlYbAyene652X3VKmsxutrVwFQ56ZRUAgi1LQFpKTsIphQw2U8lxNxbUd9fr2If8Jn86SmyQCb6ttPyWGB01gdm+ncb9038TS8UmL/aW7qU86ra4o/GrnjQcWNilD40ifLRseV8ddNYy+OuhKvwpjE4ruonKe2uiddTkvrjrSz1j+VYcYoQuO6iy1HXm31GgGO+oodOjPq8gxCOZOhv8d1+FSoyJDRQr4HhUN9yE+Y7/AFb6j9RmvFSsgOocjS1NqChS0IfaH4U4lSFFJqWpS2kA+qdtIJQtKhtBppwONoWNhHJir2RjINq/y5FvqU2hvYlO6oUMyFXPUG2pb3NmOiNexNEqUSSbmrkb6w6Up5BSvrJ/clwXbWOyoysyVHtqT86wr7dqdJ0zXaFVf9USe6grK08eClVGTYudhCfAUn5//mq/L6xOxCQmU4ltyyU6qwxDj01Tzt9Qven8Ujsulqy1LG5IoutYg4E8wPWspZ1WrElehbZTtcVl+G+rWFuVa0oTmUbCpEtTuoak8iUlSgkbajsJZRbfvNEZgQdlSWCyv7J2Go0jQuX3b6BB1jlvUBejkvNbldNP9axARQ6LwVOrIvcVGnv+gPN0IYUrLqrGUFDrDydo/pTGKylPthWWxVwofKyHksNKcVuqAyuW+qU9svq5IeR7EZBd1qHVBqyUBWVHhUCaZSVkpy2OynYrDq0LWi5TTrrTKMy1WFSsXdXcM9FPHfRUSbk6/kY02Qx1VXHA1ExBmRq6q/ZqVCZkDpDX7VMtlplKCsqtvNTJy3l83ja+JFHCUJjHX6XbmrDJKn2On1km1T4gktauuOqawuYVDQOddOz6g9qdXfjyxQQwjuqQxpU/aGynR0FDkwh/rMnvTyTn9NIUdw1ChUeMp9wJHxPCm20toCUjUKxi9muGvlwj55fDL+5UYZWu8k0+rNYex0j8TU42Qgjbesn6tk+xTZVzVwHWQQqoa+uFbSc/jSU/rP8AMfy+rk0slx1R9pf50lOVIHAVKw9D50iTkdGxYrC0Psl5p1vXmzZ/avT6s+Ing03+KuWVJ0IsOsa00lYKrqI/Ck2e1WAX+dWvUWLok3V1j+HK82l1BSaLGQq0moA+PdUR5uwaspJGy/mK9G/Gc+3lP8VTlyUNegRmWo27u2m8KljRIVI9EFZyO2iAdtOjRyV9jlJ1pB+VlrVOmJYQegnbTaEtoShOwDknQXQ7zmP1t4rypLUnRiP6TjWHRTHZ6XWVrNTJzcZPFe5NPSHX15nFX+UvaoOK7G3z3L/vS0pcQUnYoU0ThkgpcTdtWxdS8SS4nRR7kq31h8Xm7GU9Y6zVqxOOWnEymtt+lUZ9L7KXE7/l5cYudNG2i24DrSajxVqIKxZPLNj5hnT8aIsabcU2tKk7RT+KqcaypTlJ2n+3IlKlKASNZqJHDDQT62/klRw+0UH4GnozzJstPxptpxw2QkmoUXm7dj1jt/clx5tu91i9IkJDPHKi5po9FYPSKttqedVlGdJHVIpRAQVdlNLukWTfoWNIWEuMK3ZEg/HVTrgbeBJtst/WgoHYfqyk5gRxqZhnNkF1LmoH41hqlrhoK1Ent5DSDd+Wr/iW8OWZ9JVfsppLaWkJQBltUtKG56g1sCxTEVIdW4faOXzZ+xs6rhVaZUmY0tQCLC1uPmTPo6zwsfA0k3APJMKhFfKTY5DrqLhz0oaTOAknbvptORCU8B8piMnQR1EdY6hWExtGzpD1l/l5s+amKjVrWdgpa1LUVKNyfNbYedNm2yqjBUj515pHZfXXN4v+NT/Ka5klfzclpXZe1OxX2eu2R27vOwyeUEMuno+qeFLbQ4nKtII7aaix2vm20jlcQlxCkK2EVh6lxZa4q951fJuGyFHsq6k7yKEl8ftDQnPb7Gk4hxboT296TXPmOJ8KEuP7dCQz7xNaVr20+NSgBIdA2ZvMwrRaRa1kCw1XrTse+b/mFGVGH7ZHjXlCIP2wo4nD9on4UcXY3IVSsXPqtfjSsUlHZlHwpUuSra8r8qwpSucK260/uKtWVCj2UFZlHVcEi+7ZTzucaJpAA30Mw/8ABTitQSbkbAK092cpbcvltspK3CmwTrFLStWboWF6U4pbaQtvXvptw6RPRynu+r4v9CV94Vhf0Jqp68SElgRx0N//AH5GetI/zlcs2PpBnTtFJkTmU6MLWBwpKC36Re3cN5NQ5BQrIo6j+fmLWlCCo7BS1PSlWA+Fc2kt9PKRaocgugpV1hyy/oz33Ka+bR90U8rE/KSQgei1d1ql/RX/ALhrB/oQ+8flZP65iKWR1Ubf60BYW8yTIRHaU4r4DjTzq3nCtZ1nzACTYDXWiZi204zObm9w76Qt51Od1zRMD2dV+6s0WYpZWyUhI+cvr+Nc1hFou6dzLe3Vq8aJo1oaLmYalk1meQkux3itv1kK1kd9fq8rUkaJ3h6qqWhbailYsR5uFTc40Kz0h1fNxdk9CQnak1GdDzKHOI+TsDuosNHagUYbB9WlYePVWaVCkDcD3UpCk7Ukctqd+cV5gHmIYec6rajTeFSFdYpT+NIwhodZaj+FJw6In9nfvpMdhOxtPhVh+4sw5lBq/q3qO0C0c+vObXptKLbKey2AAppnd/MRvPDurK2NVk+FOtXH5dh/tSQhxCSGwd+WktNm90ooMkOLAJ7KjO50d31VSrJJ4CpWJPSRkygJ4VhiVphoCkkHXyoFpEtP/Ev48qgFJKTvordQSnOdVX5IUjSJyK6w/Hlmj9XX8Kw/Lolcc2ur221A+kOEbLHlmfR1j2rDxNJFgB2ck4K5o/YXOWouJPRU6PICn8aQrMhKrbR8nJd0LDjnAVgzRyuPHao+bikvTP5E9RH5+YKJTDTlHz5Gs+xTC0rZJlJzNoOpXrX4U8yqUrM06lXBGwipDbjEZtkIVc9Jw2/CgD5OX/nCoiVvNOsFJ9pB4EU1GksKDilpa+8f6U6plDa34qRcmylez3Cm3EyE6J49L1HP6GloU2spUNY8xClIWlSdoNRnkvsocG/zHmw60tB3isHcILzCtqTf6hYGlw2VerbupcFwdU3pSFo6wtTp9IrzBTUV93qtnvprCPer+ApqFGb6rY7zr/ctxSjKVmTst4UyElS7HUEjxrm2u+k76VqdUCTqcSL03818K13zbqFtGb8Kau2pavtE/wB6WzqQhJG0ntrIUO69ezX3VDvfVsyjx+rOeifV9hf5GkqzAEVNl4i3pShlIQj1zUVctExCH3gsON3TbZUgaPETwdb/ABT5k9uywvjypUpKgobRTDweRffvHIQCLGkQ1NSEqQehfXUltTrWVO29R2EsosNu88p9JJit/bzH+GsRUlLaSZRZsd2+o0jFXFdABSPaWMtXsNdKOmlH7TlDZ8njLlmm2x6xqK1omG2+CfMnv6CMtW86h5rS1NuBYtcUbkknaaW6taEI9VOwU3fMCE5rHZS5c8KKruJvu12rylN97+AryhMuDpjTiytalHeaaeW1my+sLEUErVsSTTxfXlLiTqFr283B5GR0tHYrZ3+a9+rYqhe5f9fqaglQsRT1tM5b2j5mEobU6vMkGw1fudNFihfwNIyq6PHb21o021OqHDXSrknMdtgf70hzXY/Ef17q9Hxpbt1ZU0rKhKexQH960gOVV7HLYGi9lKbjVawqK3kaF9p1/VpuFvuyVrby2V21huePOUy4dotWIRnZBSnShDFrr41Few1h/NpnFeqgkdFNYmj0KHk7WlZvhvoKBFxyyWtIyob9o5NZNqkQn46UqXbXTTrjRuk1FkaZB9obfPw9Gkfef3DoJ/rWIuw3ncpYcdKNRKN1Q47bhQ5GmOWSrpIVWLqU7IYjo2/3qLhMhuS2teXKDfb8pJ9PizaNyLf383GXsz6W9yB+J5cFSkuvXHqisiPZFZEeyKkoRzd3ojqmsNgB8519QfjSG20CyUgVanIUZxQUpsXBpTLWU9BOzhQQVrypFyTUTCmmwC70l/gKCQNgq1SMPjPDq2PEVKiuRnMqvgePK2strSsbjem1haEqGwi/mY036Nl3gq1MrztNq4pH1Jw5UKPAcgSSQBTuHyGm85t29nJhhyyh2j9zlJSoEEXFSY6GWVFvMKDrvbWkV7K6O7Uo/AHbX8K7d1AfYX/KKJ19RXgKzu67JIHdTEZsZFkHNbf9YxYFmSzIH/hFT8z+HOaLem9PzIBw/QtWJUmyUAa71GQebNNubdGMwpsaFxcdXq60dqfMc+cX948j0t98JDir25MN6zvcPOfUqwQjrrNk0ObwozYUuyRqv21HfMLOlxsqbUoqS4jXeoAu7KklGRC9gPZvqAOdYi9J9UdX5XD/AEuISHO/zCbU+5pHnF8VcseS9HKi2bXqC8t6K2te03/PkmYhJDrzVxluRsrDLcxZohRSbG1Lj4s2q4cUruNMYo6hYRKRb7VrUZDGU+lRs41gzIK3XeGocmI4ithejbAzW1k0xjD4WNLYp7rcmJsB2KrinWPMwhzNEA9k28zEUZ4b3YL+FYUvNCR2XH1LEV5Ijnbq8eTCY1zplfw0RcEVKZLDykeHdUdeR9tXBQ+ouKKUKUBcgbKZfztgrGQ8DTz7bNs6rXoYl6Q5h0N1qZlMvdVWvhyaRHtDxrSI9oePIVJG0itIj2h41pEe0PGitI2kVpG/bHjWkR7Q8azJ4igQdh5M6PaHISBtNaRHtDxoKSdhHJpEe0PGs6faFAg0SBtNBSTvFaRv2x41pEe2PGgpJ2EVnR7Q5SoDaa0jftjxoLSdih9aMNnXt8a5qz9rxoRWFWIKuPWrmTN79L+auZtfa/mNczZ7fGhFYBBt+NJUk7D9YnyXnnlBeoJOpNQEBERoZ82qpi9DIQ3GjI0znrWpDpjOh5TpL+lyOoO8VNjKeSFt/OI1p/tTLgdRfYd44GluNti6jaufRvb/AApYjqWoh/afZNZGff8A+k1kZ99/pNZGfff6TUV1hnPdzb2UJkdRtn8xa0oSVKOoVBjqKudOjWR0E+ymnZzb07I4r9WHR2dFSqEB5hWaI/ZJOtCtYqYLxXRny9HbUOS8y6nRbz1eND5Nw2Qs9lYInovr4q8yWvJGeVwQfNwv6C1/F+dGpn0p/wC+awiWkDQLNvZ5VtoWLKSCO2puFICC4yNm1NYMP1T+M8mK35653Dka1to+6KcHQX90+Zgi9byO4+Y8nM04PsmsEPoXk8F/UsYcshtHE3phovOpQN9NtpQhKU7AOTE4+kZzjrI/Kr1HXnZbVxSPqEh4MN5yL0pAk2laxl3d1LefmupT4CvJS7fO6+6moL+ny9XL61STkjuH7NMsKeWEJ20vDX0JKuibcKgPrQ8lF+irdWJLvKUOAtSMPfcQlQy668lSOKKxP59KfZQKZw951sLGWxryVI4orEOgmO17KKhStC7r6p21KXljOq+z+dYe3mlI7NfJiqtbafjTMJ55GZOW1PMPRyM3wIqNKWuI8VnWgVDRmlNd9YnHuNKBs21AloaC0LOraKfeclui38IoR0xIjqvXy6zTLKnXAhO00MKkcUVGiri6VxWXqVHTnfbHFXJId0TS18BQ08t217k15KkcUVBguMOFa7bNVvrBovOdKzu8Dq0pxwZ/SqsN+Wi48nPd7YgHq8aStQzWd1avV3mmFOFawpWzdTpXmFnCNWy1JecUFHSkAJv1aCnteZ7Yi/VpkL0p1nZfZ9YxmNlWHwNR1K76i4m7GbDeUFOapLAmMIUhdlDpNrpxpUVYzhL8p1XR1ahTcibHebRLyEOagpO41Mhrzadjr+sn2qmuJcLduBuDu+QGwciloQkqUbCo8VchYddFmx1Ece01ict6MhsoQkhRsSa51EQ3zWTG0Y26ukNe+oUcRmlHTFSDrTfcKmYk6/nbFgi+rjWDRszheUNSdnf8pK1R3vuGsGH6oe1Z8zFT+oufD8/Nwr6C1/F+fJMH6099+oeGx3oyHFFdzwNSBMhWLK1Lb3hWu1NY37xr+U1HlNSEkoPJh+VPOWh6rp/HkxltQk57dFQptsurShO00kWAHCpbmjjuq+z5mCn9aV9zzDsNYN15I7R9SfhMvqBXfV20xCYYUVIGvlIvXkmJwPjTTSWkBCdg+oONoWnKoXqatxhZQi6W/wAKwtDa0rJGsKFYhKfaWgN8NequfzPb/CpK1eT0Zj0lWqK+lh3OU31U/imdBShu199YcwpbwcI6KafOkfcVxVSTiKQANJaoJknPpc3Zepi80p3vpKp6UgJC7VBVLK1aXNa2+sSVmlK7BTsUoYad3KGuudkxNCeOrurCAdI4rgLcmIqvJI4Co09pllKMiqmS+cFNk2AooLGHqzCxcUKwsXkE8E08ptLStJ1ba6O022VhSGtFnHX31iSrRrcTTOmCrtA3HCtJiP8AxKmrKIRvtIArDBmlA+yCeSQzpmVo40YsppXUPeK51Lb2rV8ahSy+khXWH1lTIObXa9BoXXwVupLCEqURvGytEkqUeItakMpbKsu+ltpcFlUlhCSbbMtrUI6AVW2FNrUluxBzX6NvrDrSHW1IVsNDC4oZUgI1kdbfUCQYryoj+rX0TU2O8XmZLNitv1TvFBqZLktLfb0bbZuE7yabxTQyHWnl6RAV86Bs7DU3DWpYDiTlXbUrj30+07GVleZA4K3GsyfYTWZHuxWdv3Q8azte5Hia0jXuR4ms7XuR4mmZbTthsNF4FWRoaRfAbu+mIBzByQQpW5PqinpzTyX2GHrO5dX/AGqG+Xo/NJOxYOjWePCsIikNu6ZrpZst1a9QrEJS3nBEY39avJkUsIbKdYHW30yyhlpLadg+Um/RXvuGsH+hj7x8zF/oR+8PMwRILr1x6ooDklgc3d1eqawv6CzyLhxl9ZlB+FNMtNCyEBNSH0MNFaj3VFmlmQXDsV1qbdQ6gKQq4NFCVCxF6Qy0jqISO4cmKTg76Fs9EHWePmYP9M/hPm4R8/J+TcdbaRmWoAcTTTzTyczawocR5uYcav5tx8hmTx+SxCOXmNW1Ouozyo68w+IpWKptqb11dx93ULqVWJqyNx2+ysPitPNqU4m+vVUlgsPkbtopqQlcQuDcnXSTYg9t68rn3Y8ajYgXlKGQABN6Juoq7b0MVVb5oeNRpynnQjIBUjpvuHiqtCksBs7MtqebLLhQrdWFp9ATxVyPK0khw8V0MNi2HRPjTcSO3rS2L1iytTafjWGZG2nnFGwvUmUqS5lHV9UUrDbRSf2m3/tUF/QvfZOo1iy/mk/Goszm+bo3vXlhXuh41PeLkVgkWza7VEkc3KjlvevKqvdjxpeIlDLS8mtW6vK591+NSZvOEgZQKwxhSEqWoWzbPlwtJ2KFFxCdqgPjWna9tPjWYWvfVSVoVsUDykgVpmvbT41pmvbT41pmvbT41pmveJ8a0zXvE+NBaVbDfkK0p2kCri160zXtp8aDiDsUDRWgbVAeYVoTtUK0zXtp8a07XvE+NaZr20+NaZr20+NaZr20+P1DFXw7JKQOpqvWGuaSKjp5iNtThKLBEe2Y6u4UWo+HYeoEBX/UqmZbkRASpK3X3elox6tMSWZgW2tqyh1m1U/gjKtbSijs2incKmt+oFj7J/vSmXUdZpwfw1lPA+BoMvHY0s/wmmsMnufssvao0zgiB884Vdg1CkLhxyllJQk+yKQ9iMxK3mChCATlSdqrU4yHUc8S1rBs8jt4ioWG3bIdOZoqC2/arEHwzGX08qiOjWFSQzJ6Q6+q/wAtLF4733DWCm8Ujgs+ZiovBd7LH8fMjSnYxUUW115Yl/Z8K8sS/s+FLxWUtCknLYjhTGIyGGktpy2HZRxCUp3OF2OywpONSE9ZCT+FKxp8jotpHbTrzr6rrUVGrW20zIeZN21kUnG3xtQk0ccd3NJ8afnyXxZS9XAebgo/WVH7HmHYawYdKSe0fI44SIWr2xWCTs6ebrOsdXurGPoDvwrAvoI++rzMZmutFDDWpS9poYFIWLrkC57zULCZMeU24XwpAvq1+YrYaiRXJjziUuZbXOvvpWDz2RnaeuRwJBrC8TU6rQP9fcePmzsSfkP83i34at9DAJShmU8nN41hcaYwFh9y49UXv8k9BYdNyLHiKGEscVU1HaZFkJtS2GnDdaAaQ2hAskAClstr6yAaDDICgECx21zWP7pNc0je6TSWGU3yoAvtrmkb3Sa5pH90mkMtIN0oArm0f3aeRbDThutANJQlAskWHIIse99EnlWy0s9JANaBnLlyC3Ckx2UG4bSDyc1j+6TSmGVWzIBtXNI3uk1zON7pNKYaVYFA1bK5pH90muax/dJosMqABbGrZXM43uk0mMwk3DafllKCQSdgqdiL0lZ6RDe5NYB88/8AcFY19OV9xPIn/Y//ACaQtaDdCiD2VhM5UpspX10fjTzqWW1uK2JF6lT5EpZKlWTuSNnnYB9Gc+/WKzzFbCUddf4ClurWbrUSe2v/AGj/AOt/08mCfTh901j/AM+z9yoU9+MsdIlG9NIUFJChsI1Vi+JKjgNN9dW08BSlqWbqUSfMvyNfNo+6Pl8Rw4PekbHpPzpDj7SilBUlR1EVDxJxlWglX7Cd1OxWZKmXCbhBuLbDWlbh4jJckXGcDIr+lKLbrLkyMCHVJsL77VCkSczRQ+p65s6hW1NEgAk0xiTD7gQAoZr5SRqNqtTk6O3JTHUemaMoCYmOU7UZgaWXn5b8Vx0pAspOXUbcKhMtx577Ck3uMyFHbamkT4JcbaaDrZN0a7WqDHVHZXpVDMtRUvhUvElLOgi3JPrf2qRzku2dzFeysNw0M+kcHT3Dh8s4LoWOysEPRfT9oeZLRnjPJ4oPnMOlpwKtfiOIp+OB6VvW0rZ2dhptBmtZAPStjUeIoNxo6ruPFS0nqo/vUp5pBS4iKghwZsytdCWvmSlaNr50C2XVUSQFqKlx2rNjMVAWpfM31FQcU2onYrWKLaoTZK0+lXqTwA41Hj6UkqNm09ZVSHdK5cCyRqSOzzsER88vuHmPqysuH7JrBE+gdVxX8jjn0L+MUqOtmNFmNfxd9TJKJWEKcHZccDWB/QR99VLVlSTwFNT1qdAIFieTG4jylNyGxfKLH+9N/wD5BZIzsXO+xqJi0aSrJrSrgeSdMMcJCRrPGoMoyEG41ijsNYH9Lf7v68mIpDGLNLTvymhWIz3IykoQBci9zUGUZLOcixvY1iCy3DkLG3JX/wCPsJyvO775fl5MlMdvMfgKDuJrTnShAG4VImyGmGiUJDijspyTiTSM60N2p3EXMjBbSLr3GgvFPZaqTJDDRUfgO2oM115xaHQAQL7KlSp7F1FLeW+qm35+XSOJRky3prEV82LroF72SBQdxRac4QgDhTeI5ozyymy0CoM8vkoXbNupOIuaaRcDI3fvpqXiD4ztpatUdUnKdNlv2VLmPNvttNBJJG+nJk1gpLzaMp4UZriZiGzbIq1uOupszQJASLrOwU6/iSEZsrdgm5piTiLyQpKW8t6kullha94FQ3nHmAtdrnhUp6a0VKQlGjA30xIxB4JUEt5SaTNmvLcDKW7JO+m50hMgMyEJ17x9RxH6DI+4eTAPnn/uCsa+nq+4nkH+yP8AkcmA354v/LNYhGckxi0ggEkV5Ale8RXkCT7xFeQJXvEV5Ale8RXkCV7xFeQJPvEVhsNcRlaFEG6r6qx36Wn/ACxyf+z/AP1f+nkwT6cPumsf+eZ+5V6w0kwI33Kn4RIkyVOBabaq8gSfeIryBJ94ivIEn3iK8gSveIryBK94ivIEn3iKQmyUjgPqHN2dLpcgz8alRGZKbLGvcd4pp96FJLSXQUZ7HhXQWnXYjxqbDL6G9GrKtBunhUaHKM3nL4bTZNrI31iL648VSkbbgd16ZU3DloGYPk20ZCtSc23kcLslyY4hha7q6Kx6uWlOuPtxJrScy2tTiRtpjSycRRJ0Km0IRbpbTTsZp19p43zI2VccaxWSXHsiXrt9lQobMdAKNZI61FtBUFFIuNh+oYf6LEJDff5shvRvuI4K85l8tX3pPWTuNLJeaQIhsE6y361+PbRLcrr+jf7dQV39tIivmM408MgBuhSuNBtgRi1zpFysHYacjuojIaZGkCjdak69fChoYm2zj3DcmmdIlK1Sz6Nfqq2k9lPyNIAhIytp2J/v5+FNZIaOKtfmYkvJDd7dXjWFoyQm+25+Rxz6F/GKw5tLmFtIULhSddSA7CW/GPVVb/8AtYH9B/jVR10iE0hebX2cqmWVHW2g/CsWaZYmNFnok67DjSakRWn02Vu2Go8ZthNkfGjsNYH9Lf7v60VBKbk2Aoq8oYskp6ot4J5JMJmTbNe43imWG2GwhA1VJa0zDrftJIrBZXN3nGHdWY/jyc6Y0+h0g0lr2+VxZtwobUBcJOuhirGQWSrNwqdd+THQLjV4Xp9t1L6GpLyig76maFMlCD82hIGqorsBDwKC5e2+iX5z+dtIKEHUDsq7zOIIW6AM+21Yr0lR2uJrELIhKHHVTjC+ZR1gXAuT8aOLM5OilWa2ylNOMxFKc1FxWynopRHZeb66Ei9Q1NIYkOPC4WrLTiYGU6Iu5t1QA8IyNLe/bS0uP4kvRrylOw91eT3XFpL7+cDdWKosGXR6ptUJtb7plO/w1iassRf2jaoCMkVodlYsu0cJ4qqPiMZphtFlahwrE3LRPvEUj0EAfZbvUCWywhee9yabSuXND2UhCfqOI/QZH3OTAPnn/uCsa+nn7ieRP+yP+RyYCf1xX+WanvOsxFuN9YV5bncU+FeW5/FPhXlufxT4V5bncU+FeW53FPhUTHQtQQ+kJ+0OTHfpg+4OT/2j/wCr/wBPJgn04fdNY/8APs/cq1Yb9AjfcrEMUlMSltoKbC26vLc7inwry3P4p8K8tzuKPCvLc7inwrDJLkmNpHLXzEfVJWEPIJU30x+NaV5CVNhSgDtTTacWjJSQCU22babxq2p5kju/70261IazDWk8aVGw4dEttDfWkZItnT40zzNhORsoAvxpKG2wcqQO4U5jY2Msk99WxaX9hP8ALStO2VMnNt1pqJhLzut3oJ/GkICEpSNgH1GT6DFml7l2/t5uNM5XUOj1hY9488XBuKExZ1OoS597b405JiSCC4HU2FujYismH++e/lpt+HHVmRpldmoA1zvL8yylvt2mlKUo3UST57LZddQgbzSU5QBwHmY2vostDeq9MoyNNp4JHyOKRnZEbI2NeYVAZcZiNNr2gVikDnbQy/OJ2VhcZ2NFyOAXzE+ZibMx1DfNlWIVr12rmWN+9/11DwdYeD0peZW223x8w7KRheKNrUWyE3+1XkrE3tTz4y/evUOCzERZG07VcfNxDCUSTpEHK5+BrmONp6Ac1ffqBg2hWHXl5l7flsqeAqwrVVhwrKnhVhVhWrlyp4CrDksKyp4clhyW5NXJYVlTwqwrVWVPAfUsR+gyPucmAfPP/cFY19OV9xPIn/Y//J5MB+mK/wAs0pCVoUlQ1Ea6mYXJjqOVJWjcRWVXA1Y8DWvgaseBqx4Vg7qlwwFeobVjo/XB9wcn/s//ANX/AKeTBPpw+6ax/wCeZ+5yYZ9AjfcrFwefuauFZTwNWPA1Y8DVjwNYGP1H+M/VVxmFqClNpKhsPJjLS1soyoJ6Wu1JekNag4tNMNrmygFrOvae6vILfv1eFT4XNFN2USDv7aM2U5q0yz2CsHYcS8tamyBk1X5NGjNmyjNx+p4y1dlDg2oNRXdMw25xHmTY+njrRv2jv5YLDa9K471G03I40ObzEOBDAbcSLptvqOhhqLzh1vOSqyE1JZZcjoksoy68qk9tL5pDyNrY0iiLrJqZGS2+kN9VYun40qGy3CeVmStYUNY3UhtxebKkmwuaY5q3GL7iQ4oqsEXp5LD0TnDbWjKVWUN1K5tDDaFsBxZF1X3VLjIQ8jR9RwXTSobLcF5WZK3AoaxuqA22txwuJulDZNqdkRCggQshI1HlwaNdSnju1J81f6ziwG5H9PknF5BfKT3VzlXuHPCucK9w54Vzg+4c8K5yr3DnhXOVe4d8K5yr3DvhXOVe4c8K5wr3DnhXOFe4c8K5yr3DnhXOVe4c8K5yr3DnhXOVe4c8K5wr3DnhXOVe4c8K5yr3DnhXOFe4c8K5wfcOeFc5V7hzwrnCvcOeFc4V7hzwrnCvcOeFIeKlAaJY7/8AfWI/QZH3OTAPnn/uCsa+nq+4nkSP/SP+RyYD9MV/lmpElqM1pHL2vXlyDxX/AC15bgfa/lry5h/2v5a8t4f9r+WvLcD7X8teW4H2v5aizGZSCpu9gbbLVjv0wfcHJ/7P/wDV/wCnkwT6cPumsf8An2fucmGfQI33KkYnEYdLa75h2V5bgfa/lry3A+1/LXluB9r+WvLkD7X8teXIHFf8teXYPFf8tBVwD9WKUnaBSWWkm6UJB7ByLabcFloCu+ktNp6qQPkpclwFaG9WROZxfDsHbTa3syAFvpUvqaSxSqoz+maCrWOxQ4EfJSGg6ytviKwd0+kYVtSfNxaLo3NKkdFe3v5IT2j0oUhSm1J6dt1YcYiVuaLOehcqVup//ZsS3tqprVhZvvfFYt9MV9wViJ1RBvDNMH/0yV/mCkuOIzZFkXGuo0RT5OvKhPWUd1SJLWRLDA9Gk3J9o1i/0u/FAqefRwx/wqZ/2ZK/zE1FffYQ6pDdxvPCmJC5bUht+xsjMDbZyNNKdcShO0mmWktNIbG4eZJeDLK3DuFYM0crj6tqz8qpYQkqOwUlSVi4Or5K4/cPEvoMj7nJgHzz/wBwU/hsWQvO4nXbjXkSB7B8akNhuC6hOwNnkwH6Yr/LNY59A/jHnC5NhWGRTHiJSrrHWax36YPuDkjIC4DKFbFMgHwryJA9g+NMYbFjrztpN++sf+fZ+5yYb9AjfcrHYyg6l8DokWNX85r5tH3R8riU9yOpCG7X2mmMWkF5Acy5b69XK4bIUeAryxM+z4UnWkd3JMxRtg5EjMv8BSsWmK9YD4UjF5aduVVQ57coatSt6eTE5bsYNaO2uvK8z7PhXleZ9nwpOMyxtCDULEG5Orqr4crrgbbWs7hXliZ9nwrDpapLJKusDrqT0HJSD+3R0D2jdQZTEdZdUolARrzHqnsqAFaNbhFtIsqt2fJzLxJ6JA6qtv8AWkkEAjf5jzKHm1IXsNSIy47pQr4HjUaQqOskAEEWIO+lzRo1NtMhsK63bTEvRoU2psLQdxqRLLyUICAhtOxIoTgUo0rCXCnYafeW+4VrpD5RHcZy9dV70w8lrPdpKri2vdTU8NxwyWEqHbT0ltxBSIyE9opM4ZEJdYS5k6pp95b7hWqkSFJjuM5esb3qNKUxmFgpKusk05MGiU20yGwrrcTyYZC0KNIsdNX4DzcXcK1tRkbSddMNBppDY3D5LEzaNt9YU2UJksiM4pV+vvFqQWCp7SrcvpDsvSUJ0YTtFt9ONLjXW0ro7xTD6XkZh8aWo6efr/Zf0qJIU3EdznWkXHxrDlKQiTpD1TrqEtYfQpatT4J7qy85dfU44oNtm1hTimhBeDTyla/CpDjqZSFo9VoEjiK0mebmSeiY96iCOtKM63M5PbUvVFf+5UXmxLdlrz27ag3MJWv2qbYDkAOFSrpQd9aAJw9TwUrMW+NSSRhYN9eRFOqbMlAdcKU6Eb99Z180lWWooCugo1ETFLicinM1t9/99SEtrZcS4bJI1muYYP8A4n/XUNGGRFKU3JGsb1Vz6H79HjXP4fv0eNOS4LiFIMhFiLba5hg3+J/11FawuK5nRJF7W1qqSvDpLWjXITa99Sq8n4N/if8AXXMMG/xP+uuY4N/iv9dcwwb/ABX+uvJ+Df4n/XUdGDxzdC278SbmufQv8QjxqU3hUpzOuSL2tqVXMMG/xP8ArpuVCbbQgPoskWGvhXP4fv0eNc/h/wCIR41KGFy1JK5A1DcquYYN/if9dMyIDLSG0yEWSNWulTYKgQp9sjvpcLBFm4eCe5deT8G/xX+uuYYN/iv9dcxwb/Ff665jg3+K/wBdcwwb/F/6qRYJTbh8oalvaaQ4vt1U80tpeRW2w/GsPf00VBO0aj8OR35pz7p5EdRPcKxKSY8clPWVqFMtLfdShO00zhcRtOtGc8TU3CmshWyLKG7jTDq23ULRtBpJukHjWOdVj41hUdp95wOJuAivJcH3IqfhrCGFuNCxTUZwokNKHtDlxp+zSWh623uFJaWpC1jYi1/jWEv6KSEnYvV8aW224nKtII4GkYfESrMG9fbr+UnR+cMKTv2p76wmTmQWV9ZH5ebMiIkt2PWHVNOtLaWULFiPl8Mw86nnR90ea+8llpS1bAKwttb7zkpzjq+TnMLeZyp9oUY6kSUOtAWIssUhuYyXcjaCFLJ1mtItLOZSdYGsCksOyDne1J3JpKEoFkiwpcZ0uy1e23YVzBR5qT6qbL+FLiv2kpFvSOfhT2HBKUKZvnSRa5osyWnVraCSF9ZJ41zOQWJNwnM4b2FJjr52lZHR0WWmoS2pLih1MhCfjTCJzLaUBts27akIU4w6gbSmmW8raAdyaDExlK2m8hSSbE7r1oCiIWU7clqSwowgwrbktRYmuMpjqyBAtdXYK5peXnIBRostGK+IzzAsRfoUyZmZIW2gJ4g/76fZDrK2z6wtX6Pse9V+FeQGPeq/Cv0fY96r8K/R9j3qvwr9H2Peq/Cv0eY96r8K/R9j3qvwr9H2Peq/CvIDHvVfhXkBj3qvwr9H2Peqr9H2Peq/CvIDHvVfhXkBj3qvwr9H2Peq/Cv0fY96r8K/R9j3qvwr9H2Peq/CvIDHvVfhXkBj3qvwr9HmPeq/Cv0eZ96rwFfo8x71X4V+jzHvlfhX6Pse9V+FeQGPeq/CvIDHvlfhX6PMe+VX6Pse9V+Ffo+x71X4UlOUAcB8pij+iiqttV0RUBjTSm07tp7hWNM/NvfwmsGfCXlNHYrZ8OR35pf3TyI+bT3VjaumynsJrBEjTOq4J5UMtt9VAHdyY71WPjWGym4zq1LvYptqryzE+34VOxVLzSm20nXtJqAwp6S2ANQNzyz39NKcVuGofCsPijmBSofO6zRBbcI9ZKvyqO6HmUL4j5aeyuLJTKb2X10w6l5tLidh5X8XaQvK2krNRcSakKyEFC+BqXDbkosrbuNSIrsZdljuO4/KJSVEAC5qDhQRZx7WrcnhyS3XG8Siknof31eZPeVLkpitbAdZplpLTaUJ2Afu5KUpMZ5QOsINKnS+aMDSHOF9M9lKkSCVNJcsVyijNwFqf53GjrC5JKdInKv1rHbSZjrTcpTbxdQAMqlD1ibUgSIsiOFPlxLtwb7j2VMU8mM6Wuvl1UmQ5zWUW5SlWQOtqWk1z19RgALP/F8bVzt3yl1vQ5tH/Fa9RHFrXKzG+V2wqA4tbSyo39KsfjWLSVNaIBwpvfq7eykLc5tdShmCNduNGfK5gnpnSaXWezbTj95chK5bqLKFgkX3UvnSly1okqGitYbjqpyY+S6oLI9G0R/FU555Dr4Ssi0Ykd9c8lEQk5zcH0vjasTdUhUcaZTYJNymnZLrSIq2nnHBnUVX2kClLdeamLS+sBC7ptwy06p1piKVSnfSHWreNVOv5WWLTHcqnrKWRr2UZL3NnP1hWTTJCXd9qMl4NOASlqbDqAHba9e2ucOhiXo5C1oTlyrPG+ynX3xLOaQps5howR0CKcfJmSErlPIsuwCRcU888mWoLfU2cw0dx0CPlcYfzycg2IH41h0tiNpFLCsx4cKlYlFfYW3ZevZqpCy2tK07Um9NuJcbQsbCL0780v7poGkdRPdWOA6Vk/ZNYGr0jw+zyofac6iweTHB0WPjUSIqUtSUqAsL1IwuQyjPcKG+1MaDP6YKy9lRm46GhoQMp5J7+gjLVv2D40nLmGbZfXQxiIAAEr8KmutPSFON317b1gsjorZPePlnW0uoUhWw1GdVAlFl3qHf/Xkxd1bUXV65tWHwkMNJJF1kazWLN5XY7iE9K+2hupxtDiSlaQRUrB1DpMG49k0tC0GykkH5GPhkh/XbIniaiwWYw6I1+0dvJKZxLSlbbotuSNVS3ZZ0enbtlO21R3kPtJWk8mJTNC3kT84rZ2VhkLQN51/OK/D6kpSUi5NqK0gXJ1UVJAuTqouNgA5hY1p2feJ8aCkm9iNW2i80FZc6b8L0paU7SBRWlO0gUVJSLk2rMLXvqoEEXB/cCQ2XGHED1kkUrCFnP0hrQ2P5dtKw9zpqSsBen0iK5lJWgl10FZcSq24BPCl4fmXJF7NvDZwVxpEaYVpcfdSdEk5LDfxNZH3oYClZHSnaNxrmEl3TKdWjOpvILDVQwxQcWsKGtxKh8K8jjRZs3p82bNfVe9Jjz23XChbWVa8xuKYjzmVWCm9GXCdmvXU2E66vM2Ua0FBChUSItiIpkqB22PfRwlzX0x8yE/GjGnIeeW0pqyyDrHZS4c0reyuoCXetq10vDL6YBdgWkJT/AA1zKU6H1POIzqayC2yhhigtxWYdJbZ/lqWw+tbK2im6CdtCPIW4wt4o6BVe3AimMPLMeU0FdcnLT8R8txNGpOZrjRjSXCwXSjoO5tXC1eT3OkgKGj0wWkcOIqVGLqG0psLOJV4U7AWedJQoBDtjbgaegS1lbelTolm+vWR3Vzac288plbWVar9IU/ClrLiNKnRuG5vrI7qAsAPk33Q00tZ3CjncXxUo/iaGCO+9T4V5Dc98nwqVEXGcyKN9V71gz2ZlTZ2o/I0780v7p5EdRPdWLMaSPmG1Guokgx30uePdTMll5N0LFTp7bLakpUC4fwppK1OISi+YnVSE5UJF9grHeqx3msE+kO/5f9atWIRebv6uorWmsJmaNzQqPRVs7DyY09d1DQ9XWahwHJQUQoACvIjvvk+FP4Q620tecHKNlRHdDIbX26+6h8tNiJkt29YdU1AllpfNX9RGpJNTo3OWCjeNYoYlJZSGlxznGqkkLbSSnbrsaffbYbK1nVXlrXqYOWo0tqSi6PiKcZbdFloBp3BWj82sp7NtLweUnZlVSoExP7BXwrmsn3DnhQhSz+wX4UnC5ivUt3mmsEP7R3wpiDGZ6reviddEpSCSbCmpDLwOjWDTbzkXEFturJS5vPIttC0lKhcGocAxXXCHOgdgqZMRGbvtUeqKw+It5znT+u/VH1PHB+oH76afeX5NfjO/ONFPxTfbWI9JqLHH7Ui/cKgMtOsuRX05tA4bVhsOKtcolodB+yaS+pgYutO3PqprCoqoaSoXcUi+ffenVuSMKYCla9PkvUiQtcIMu/OtPJCv71i3pTGij9ou6u4VEXfDZDZ6zQWk1hP+zo/3f6/uGSALk2rnEf3yPGtMzYnSJt30X2RtdQPjXOY/vUePIpxCOsoDvrnEf3yPGucR/fI8aS8yo2S4knvpSkpFybCucse9R40ZDNjZ5u+7XTCyppN1oUd+XZSnmkGynEg9poPsHY6jxrTsWB0qNfbXOY/vkeNc5j+9R40laVC6SDSnmkGylpHea5wx71HjXOI/vUeNc4j++R40H2VGwcST3/L4tp1spbabUq512rDoT/OkqcaUAnXr48uLRVvNoUhJKknZ2VAZmMSkKLC8uw6qWCW1/dNcxl/4dfhSeqnuq1TMHJJWxb7v9qVFkIOtlfhTcGU51WVfHVUDDRG6ajdf5cmMMPOJZyIKtuysIYfaecLjSk9DfyTIokslG/1T21zGaD8wuozjimApxCgoDWKdjznXVuGOvpHhUBjQxUJI17TyHWCKdgSkuLSllZF9RtUAumMgOIKVJ1a/l58FMlNxqcGw1BxApVoJGpQ1An+vLiN35zUe+rV+NNtobQEJFkimLN4upLezXeluBCFKO4VGxFiSrKm4VwNZgN/Lq5JMtmMkFw7dlMPofbC0bDTzSXmlNq2Gmo7yJSmgvI4Or21MfeUkNyGrOJ2KrDZWnji/XTqPJMmojI161bk1EiOy3ecydm4cf+1D6nikZ2RFyN7cwNYthq5IQtr5waj2il4euTLCn0+iQ2Amx31GgKizlFoehUjXr31AjOsmVnHXezDupnD1k4gHR0XlaqDeLNs83Slsi1g5fdS8NWiHGZb1lLoUo1imGuPrbdatm1Zu0UvDzJmuOPjoBNkWNJw55h6UGR6Jxq23fUNOKsNtM6BvKnfm/cNQBBBF6a6Tz6+YDUMpRq1GkIzRoSG0J0i1qOvq6uNZSIK0c10pAUNILHXTaAV4YlcUI7dXS6PJOUhEZbhbC8uwGnWpOR1GhY+bzaTLb4CnGUoGHrTok5myCVjo7Kg6FU2SUBBslGsbL77U8kLbWCL6tlNstLjwMrQJ0nS1cONSNHeXctN5NQbyDpaqgpSmGxYeoKxVI9AdBnOkTr/pWibcfmhTGjswNWq9JebbiZnGWVrV1Up7dvdSG4wOHM+jUvOc1tdFI0079RJFrDZq1Vh6QmGxYerUnQh1rOylWbVmNMtJ56rSx0N3a6Kduyo7SXF53NiM+vIAg0pCBhkQpj5iVjWB21FSk4g6eb6OzQsNXH/fM2A3JTwXuNR5r0Rehkg23GkrStIUk3HGsRjPB5EpkXKdopeNdCyGSHO2sLiLRmfd66uNYovJDc7dVYc3o5kf7TV6xF8vPLUnqN6vjUBJTEauTe1/Gpyn1YglpDqk5rVIZmQ0h0SSrXTDmlZbXxFY1bNGHbQUcNl5T8yugQRcHVWKxyUh9vrI291NZZkZBdb2jWDTEZmOLNptU3E0M3Q30nPwFQ8PcdXp5Wvgn5dxxDaSparAb6YnxH1ZW3QTwpMlhTRdCxkG091c7j2aOk+cNkdtJfaU4ttKuknaKU+2hxCFKspfVHHkfmxmFBLrgSbUzJYfF23AqlYpASSC+m4puUw4vIlYKsua3ZSpDKFhBX0iLgV5Vw//ABCaEhku6ML6dr27KdebaQVLUAKYnRX1ZW3QTwp3EIbSyhbwChuozIwZ02lGTjWkRkz5uja9657F0Om0o0d7ZqaxCG6sIQ8Co7qakMvZtGsGxsaVPiJSVF0WCsvxpGJwVqCUvi5Or/f0saDNJTe9rEbu891RUsrQiK8ErBuptQ2Go0ZMdCkIPRzXA4U7HDjrCyfmySPjTCHkuSCtRsV9EHdSkhSSlQuDtFJihLK2gtWUggX3U5oo7DaXEZkDUTa9u01FdTz85FNKDg2I9UJ2cj0daXkOsCyir0nAinWEOBVwLkWvbXTLeiaQgeqLcgjpEhb19akgeFIjsoJKW0AnbYUqG0VtKACcir6htpSApKk8RamWg00hAPVFqdZbeQULFwaZhJbc0hcWtVrDMdgrydFuegfu3OXwqPHSwwhoG4TQYAkKevrKMvy/N3ONc2c4iubO8RXNneIrmzvEVzZzjXNnOIrm7vEVzZ3iK5s7xFc2d4iubOcRXNneIrmzvEVzZ3iK5s7xFc2d4iubO8RXNneIrmzvEVzZziK5s7xFc2d4iubO8RXNneIrmznEUw2UXv8AUZEZp9GVYpTM3D1FbZzN7/8AvUXEmH7A9FfA1lTe9herVjZ6DLftKqepUeU3k26HL/SnmdGmJH9ZRzK+NJFgBwrEA55Sa0ZsrVY0rD5z5GnfBSKQgISlI2AVjAKpEZI2/wDevJC3Ll2QpSqw1uW0lTbqeiOryPSWWE3cVanJ0qYrRxkkDeah4Y2x01dJf5fUMSjLkxShG29++oklvTaJyMGXgjVq2jsqO4XA1GXdLJfVdXtHhWIgCRhgGzTCof8AtOf/AA1O/wBp4b/HyPgKxtgKAPoTtpxtEfFoxaGXSJOcCoSlgyMsHS+mV0tX9amjQS4UkCw+bV8aY/WJk5/1UJ0aawxS9A2OYZxm6+qmx/627/kisQSHZ8JlfU1kjjWLtNtIjvNpCVpcFraqU+y3iskutFd2xqCc1OMrRh7xUgoS5IBSjgK0q0wTD/aaXQ/CiMuBuDhIqIpSl9KAGtXW1VCWuKsyP2Snihz+hrCkNuNysyQoc4Vt11grTeR85E3Dxsbf7/sPPS02i+VAHcP9xXq/mXHmXB8+/wBZlYUw7rT0FfhWfEoOpQzo8RTGMRl6l9A9uygW3RqKVDxpyIw64lxSLqTspcFCpaJBUbjdySITjkxp4KFk25XIrLjqHFDWnZV6enxWus4L8BrNLxKU+csZr+ppnCVuKzyXLnhTbTbScqEgD6jKbfcbsy7kVfbamYMgyA/JeClJTZIA1UjC/wBRXHWoXKyoEbqVBkL5lndSSyu5PGlwZyZTzzL6E5+Ip6FNdMVzTo0rWbXbjUVExObTupXwsLVLhSFzESGXUpIRl1i9RoC0v84fe0jlrDcBTcDEWC5opDYClk7KkxVyIeiUoZ/a7ahwubxNFe513PaaYgYkw2EIkt2+7TsGZzsvtPoSSgJOqnMPkPNJLj40yFXQsChh8l51tUt5Kgg3CUjfTcNSJ70jMLLSBap8VUpgNhVukDRw9BniVf1dnbxo4U5zFcfSC5dz3phjEUupLkhBRvATUbD8kd5lwhQWonxrDYRhsrbKgq671AiKiodBUDmWT+801/QRnF9mrvrDVORpGhcJ9IgKHfTxPOcS/wAj+lYf9DY+7TL+hkYm5ty7q8puDQrXHs0vYb05NWZCmmWc+TrG9qbcHMpKlpUfT7L2p2S+hQS1HzdG5JNhUOWJLWfLbXYipRVInpjZiEBOZVt9NwlMSEradIb9ZJ115SdVpFtRyptB1qvXP0lUXKm4e38KVLIkuNZOq1nvXlR7Qpf5r6Leb09OIdQ0y3nWU5uFhUmSFxLusLBDoFr2pr/a7n+SKxhxxLCQnYVazQlFhLMdtglwi+XNs+NIxHoP52ylbQuU1Ekuv9Is5UW1G+36tansOiO7UWPEaqVhDzZuw9/Ss+MM7ioeNDF5CfnI39KGNs721V5aj+yqjjbHsKo42T1GD41z3FXeozl+H965hiL/AM69b40zg8ZGtd1n8KQhCBZKQPq72KRm3CjpKI25Re1GdGEcSM/QNMYpGdcDfSSo7Mwten8TjsvFpWbMBuF6TPjLjrfSq6U7eNN4tDWpKbqGbZcWqTPjxlBKiSo+qNZqLOYk3yHWNoOo15bh/btfblrTN6PSZuja96RiUdyOt5OYpSbHVroY1Fvazl/u0iY0t/Qi+bJmp3FYra1I6SinrZRe1c9j82MgKugVztjmvOc3QtekLStCVDYoAj4/vTPjuyXWGrHR3upVPYc40W3WVLcWlWwndTjD5enK0Z6bVk+FQkLRFZSoWIGyjGkZsS9Gen1e2pEV9UGIgIOZJRcd1aOVGlvLQznS7b4GuaS+ZvpLXTU9e1SGHjKuuOp1GUZBfUDWGMOssKS4jKc5qXHfTJRKYTmNrKTTXP3nwpY0TVurxpDc2M07HSxmuTlV30qG+w3DKE5y0ekO+ktynJT7qmSkKYIFGK/5HDOjOfhTjMhiQiQhrP6IJUnfUhE5+IczWvSAhI3Dtppl0Yktwo6GiAvWIsuOsoCE3OkBqQy+3LRJabz9DKpO+lRpTomPLbspaMqUb6hpUiMylQsQgX+tWFKZaVtbT4VzSN7hHhQjsDY0jwrKngPrS75Vd1YHl5nm9ZSzmrEQjn2GoI6Fz3XrHgnmrSh1w4MtLefaxZ9aGc50AuKbF8MnyLj02uw3VllTIcRhMbKkBHpD2VBCTik8q6wsE91OWGONZPWa6dNSH2oDiNCMi1lOc7r1N/VMLaYz9ayb/nWGvxxOdaZPQWgEd4pj/bEv/LTS7jGH7beb1goRzEEbSs5q6sfF0p6gXqp0qiRXWD8083mbPA7xUL6JG/yk/l/8cKwohxamJK2gvrAUvDWlxkMqWro7F7703hfpELfkLdydUHZSYiRMck5takZbUMLQG5LaXCEO7uFMM6JltsG+VIHhUnDg68Hm3VNuW2jfUTD0R1rcK1LcVtUabw5pMRyOSSFXpOHDNHK3SrRDUDT0JDj7LwOUtndvpERKJTr+Y3WALd1czHPTJzG5RltRwmy1liQtoL2pFDDmRDXGSSArarfUmA1IipYUersVTLeiabRfqpA8P3nQG3HpOmlrRZerXWHyChuSVuFTSD0VGk4n1CtlaELPRWa5y43iEoBK3NQskUnEmDGU8bjKbFO+9N4l6RCXWVt5+qTUeS+ubISpK8uy3s1GltMw893FXXYA6yTTc/pKS6ytshObXwprEi5kPN15FGwVt5HFuqlOp0i9NpPR2Oq1DYKnv6GM4redSe81hi3G3HYzqrqFlD40zLDrj6MttGbVKxFxyI0toKTdyx/tTk7RpaGiUXV/s99IxBJQ9mbKVtpuUGvK9ghRYWEK2K7aYn6R4tLaUhVri/ClYmUjOYyw3e2anJT4xFCQlRTk6vHtpqQ027OUVL6J13P5UnE9bekYWhC+qo0vECHnWkMKWpHCospElrOkb7Ef/F0aGHFTdM1tX0Sf6U2xKXEkQ1pN09RW40vnUppmNzdSLEZlHZqr08edIc0C1oIA1VzCS7EfWUWWt3OE05zia5HTzdTYQq6iab0rOISLsqKXdihspuNJ5m0oNnM29my8abkSn1LtGyt5fX3mksvBaNAw805m6WvoUsKKFAbbVo3gyljmrgeSu4cFYWl5LBS4hQIUdu+pzT0mUy0AoITrKu2lxZEeQw+Frd12VxtSdPHlSbMKXpdaSK5tI8loTojmS9e1O6cPsTUsKIyZVI3ii1IfMuQWim7WVKd5p5h3yfCTo1XCxcU8295SC0JPzB17r0tuQ4wczL6ngekTs+FOh5qdHeDKlJ0WXVRhvveURlIzKBTffTvOpaGY/N1IsRnUdmqozTiZ0w5TYgWPGsJbcbZczpI9Idv/AOsu/wD/xAAuEAEAAgEDAgQGAwEBAQEBAAABABEhMUFRYXEQgZHxIDBAobHwwdHhYFBwsMD/2gAIAQEAAT8h/wD4H3DwRetDwhR94NpRnONpgKeF02N46FiWP/hA0PqqbQ7CxSKrZK8Lg9IDWfzaE1deDL/41odfm9BMmhFZ9q9oTPSnFgW76Q1dpbfccOk1QtH8kZkmJhsrUqU4ien5v6fWgqgDdg5nzX8cy0IDlmF1Da6zMD4sv+k04btSs8JOmrCI/IPFsMe5wUQtywNkH0aCFWjRGz/4stHen+Ue/MR37y8M1Apo26xc1kOqtSzomUUKtqhrNbC8wurpcyWbLLXBk1MXLFOZidyEuJrtCDyXsVn6q4hXTTygMEN0q1DFzlZfRiVNr1/1AYKB5AQGnXWXPvKm+0y9kPG//DkrSSo31E7A1WmXAuvL/ZsZTqsRde7unmRUO6h2/wDimcq01yLHRjZlq7wtNghatbI8W8vFDmPM/X/YmLEVs43B6zoNYNPNRKxeDnB7Edsg7Z4GKmARhowlxshWtL6Tgoi9G7HeC/qC40CjSq8xMU0PG+YSIWc58opObV94eGl3WIDafP8AiX85KhBczquvSaNPswnS4Rf53foziwuXd4BxzgbZf647Dt2VpLLynx6Qt61rvf5gwQ1XBLMJ5Nfq7n2MAmvyfsvgFry8sAljZz9a9QAysBBetHxjoA1WG3VoH/FrCu9KNuLpXvyiBjZNNuEwAzc8cCLD+v8AFHXtZWRcTHe9Vyk1kGxUc5Pbt3gImDWomUx3ZVLgar1hwTSZUgdW1TXk1XK/TrLPHz36EVs1muHpNYPg/wAusCQsW4TlkS7cmIKXGN7cQSFP7BUMBPQVbCao3nS+0bp+qIiQNq0uBUDOGocNzNtWbR7boqluqSL7IEQ1CrOsCo823dMimBswd3eDYsu4/qXsJ5n065AOWXq+HT6xdh9j8tJxI/rUa9HaNY89UJlnGNA3kMu6vuy6tPevzh764CUp/R+qNXQUxvYaf6nuat/ipOYdktWYs82H/FoOwk0PXuRLIBs4Ctp2lunFMKzciHTBooP5XLTHS9AtFgmSmbR6xdYrOIyiKmV6D5Qu1FtzUKwD3sHQ+oHRQp85rjBQ2O3eZsCV/cIrJ247ZgF63dxrHtfmfSVMGG7SY3yRPLwWgO/30gH+iL7Hayehb+FD376comGxivXhcGNYD+IoVbU9Zc7+Gex0lIUUjvMlb05MZ4Fv0rZADVY/3p+szKKbP8RQr+t0h9ADg8H+gWAX4KxE0qVGRla7ICDC7aWC1AFjZD/Mt51uEfzB36Rd5SHyNzv9KvOCOQLfN4OkAA2O6L3Oj4AcZ6miAuoQa0fua8KCdn/MAmfgNpUaJVqGv6Y6FiWP/EdE0zNp5fJZMYjgFdihJy+txudYUNAKWXwXt8JuS6VF5WdufXLEKUDOxyXxASAuUG24ROadN7W68/UaJpgOV2mkYOVcye9lHS2/WNhPzXrJomKb90UzHV+ea1J2zs2l+NMp8CLmfGZ84+wtoTE338BeGXH1o+yYqYFodthBmOS/cRf3Qbx9Hq6ehqwuTJ+us14bsngrCkdGY1VZ9auoSRVUdIYNGEXKzAOJ5Qqo/wBzUQKAlAXuatHWFX20eJoyw+yU7EXIezKTKc8+Uq7mrYX14gj9GSNqVt1Qw08I0FnD5TquiUDqY+cvw4Ro9mEv0O+0Oo6PmwGaARAKtET9lH2lz9AfSAACg0/4jJFWFy/gLV8nhLtNRmmrabEtLGg3jaiwDte8CWVDqPJhaaMK7St2VvZ0vRp/sDsm6s3z5kNYL46mK7fTstxz98P/ALVkPQAA4CMAESkYRoedfUlTYf50BKBvyvLL8KlTOurShq63Zj8tq2y+G4ARVMnCa+LICtRltya3FFmVHZ5jEZ0P800al2kLVee73CZB+vGH0O8j6f7lxnOtHRA7ARkvs7PKJMlKZOJrI3n7ktK5ncIcLm6jqjLZ+jFQtZpLQWdeU1UGCcuWKWIIlh9Fd6PxuPQn9t5DQBubneNFpYH8wka+lOTpBrIWJ9GKOGXhp6kx0/J7wiLBT5x392Ddc/uQi6Sk8DAybeAg5X74lGtPUaESIAarFFpvf3pHQWH6ekAACj/iaiGOk6mp/MvULcTEurO8VDvO3nVjdg3VMt2OJZ0XhOYUq2nWKG+VFWpYoRqZW+VNfym3FDoOkr6aov63bnMKNbEcEFI0WY0gK8ujSXf2vvoKeatVy+FeFTXgj/gQR7NLOMxiW5YrsBMML/xR8at2ikmSgq3v/TOW5bW7g96rjm+zUerlpyraYimFsXrK0kjy+fc5Vjxz/mFj6zP6zKqZchQ6d4lH1x1ZTmFA2cTCmW/cZmPaPrKBswuql+Dn+sqdUlNeGFABSMpOvuu8WX41Zb1/pChowdiWKldT7wg2/fZHJjoZfmC6TpFY/J/UKshYn0KDLEKYFQA5Nog8l5J+gPeEQ0v9IejjHZEs37VzUbsygJSrW73nTau20dwGo8Q5sHb8mMYZpL4AIvT3F/8AFCaQuvDzjLluopq21txMimGZ/oZRay1MEMbGTuuECUtZfNjJ5w+nZsu16zaxKbs5Sq7JT8iOdoiHIudCccOhK8VRVoJerW/cy4i+g3Se/E/PjPtHWOd8rlRt4PXwvwPYbX0QMdc5w6kNCNN/KUwcFt1qU5l9eT6AVhZY8dYmqc/Ub94aCU01pTDuXUh/2oTvL6xovJ6wVxfof6jPKAW1ZbuM3PKbUW60+mp935zqPWfa0RPyffylPUdMpSWfb+8qig8MSE0HnsmNNn4kryLXzNJXucjBj6i5mrF7K9+zD6BLzLqymLTn8zqeWuGCDkmUnQ6HaKFhJ5TexXhTpmryawhrw/M8sqPT5c9CHihYdiOXRyusFCITRIrF73J/xPPC6n7V0n6LiA4BPpHQP2zkX1E/akRDh3JPpmJ5RQ7TNkzhquJuS7dmDqFC3O6imCF5OYAQ0MEvwTBDeN+Q89/A8bTglaZcjBWiklP1hIG/g9ICJY5GV4WnCb50cZVSecToW7aM1pyvyI7dMJ1RfNezA05eIcFnC7p/BBgJSx2DUGxc0AtlmtX2QWWkuUIH+4iovvMTKVquvyVT1WIGeYfxNBm0akZUHO9M3rY33bpKixesbS27heZ3Y/4Iqx7rcNvL6C49V5cYIsHaV+ipnZSGnUlx8n9MkWpWD/H+DQ79JK/wYmR5RfgG7uev/FZ2v5BlsHb3NCJo8vuVF9XDzqA9UQMP8S8o6QcSVO3qU+noFm4xvulR7B6S+PjH1ihjN1kOnSHgVAIL0jjqxrDdUMILhQWVg6e8EgDLPbqceAzd70eHmLatVjKocAhhv8LlRnC+UxgkxjvS+6Igp6Oec0oMqRi78x9SB+YszHj/AEwwKrBKl4HeHPJMir4oP4lPWb/GZ9mPcj5i2Njt8wSEaSVwhneqNOzNqRQzKyY/DniMeq/4xwmD4DzczYEZOHj5hXhcU8ycyhDe0VgHOrAAqMtCzt5JaHDEjp7JgvVXRUvCJQTfYy+vgulOvExSk+yW+sDCOV/x42f8MNSUurzGNanucQC06lNbjGCSyYs10iq0LQ7WHuLzjtBS6L/TRnP2HJpGnr2fpgW2JM4ZMMPMV5ydfEXOfaeGZbi/hMIA0GlTHNQBs8SoJ0Gx1+HRnQB3mmPa1tPCvBdZV9SdQAZiMxFAakzcBaypke6i+3zLMfl3eXxzHhUolB/TrYn9Vq/D5SEY9Zqy8r+ghuRRlPbK19Y3ivN6j4sqnhPt7RIhbCyIqq7hnxMC6THNxm9f9+W544cNMjuk0fzMw+jyon9DNgfvLdiEbfRif7pf/UlOOSvG5ShtarWEw1/08f8AUsN+M4DX+hNveca27P8AafbaP8JSlV+XOkNP+EqHZMyS0LJY3Z5Znsm3Zma2i7vV/wAkrJrOBfRwsb1wsro7y9YfXSsdesbpYSVW/wDsv+ky3HZIJ8yisBz9Pf8AT1j+/wDmZnOrHN/ZMwHhNxSYCpHcm2UimnaMd2/mHpNcbw8fA01y2L7NZDoSr3ybTvMfJ4/dpb9zSHe5/wAq3mb35vRl22b7IMAUBR8GyR5jiWzE9Oh8BNCnARImcsPuZwsw9Ad5mcejQOG6wMCG3u2YnV1VXNBvP8csC4gPSXTdfwxiuqH4dvxk7kv4DGKYX8QTdbvv8t1AZ/Fuce7M2u7lzSQ9X9z7nBDxFO58i/GRiaNPq+3g2v5gXNA/kgGAD/hdBg+bmphS8rqbEwaDFOmpNShlxVr/AFDLLo7B4jsJnbSCMETe5/2SoENzh4TyYwbNtmbHgRmNPRs7OSJnVdzuOT6XFV2Ndoxv6YZfWXvlg9/BnSr7SV4EZgVKvtq1iltZmJbYcPCV4WVdX3mlQUDs3iEX+4+IsOqOHQAHggmRgGWYgZ0bI04UNcX8seQ67zhGB/PwMyRko67n4BaAWs1i9lnY6zdSBeR5JQfnTvAM0opi12jSL/jGKxMB91KLL5nTlEru9X0rh/G62p/BKhj0nwKFVoZtkM9Hf4CCw5NrMPw/QJqQZzbzhM6Z9GMUq6z1j4HrM2w5YJbT+ryyjyu4+8AD/iWFFFqvXj7zesp6sww3F5qGXnpNBACnnVyta6HveYlBbpVbdpY+i8w6VoPT+8x+theWqQVuWEdEaqmu/D6VNYE+6wPQSD6wN1tS7O02wL4KjdQT9eJnxI4057ni6NJYwKcDyGUxUFiUks26C81/McNkN6lvrWeTxPUfJZTLFTl01G3E8/GgsOYn6u2Yg4+W+sr/AEgV2lfff4K0a9bfG/A1djZcb1aWsQ9A4Ctd3rAXNBoL+JTNq8KPWFVQFkWm62fSaiSPrNIqV2RGfZKF/EXtZ3MUOfhVdv8AY+BmKbV/Yw+iUCThnTWDxqW9ottof8a4el/yEZl8HQ4tpcQWO2XIculwc7RU9R0ueHKi1cC9cN+kDUarvfX+CawvE87RfxbdFN4FrL91qJ1QH0qQ7sZzTMeai6rLMkSoPUqhkV9jDsMZPsvmwC0Es8KlIaPsRgABatEHWnFunhmA5rMyQDRfzM/DU9jv1TU4tqJqKZ/GiKZfmNZSlWgfKZyPI/L4GKW7jxKlHlh/nk9rIb0WiLj65Q2d6EQyuQjZjTmdazZAuEAENo4oD0AdCUdSIrPb2f0Dx46theiaKzHn8GIa/eTr6Pouua+hG1XlhYWrQSk6Ng2xUrfMf8cLZNRmVYSy7JVzbe6/qDue9h/iZZabXMi93qNP5mpxWQXDfr7lRNZoLa3mDKmHPRen1A88XG7WayG5rKyDcUdUNQJBO28fV2Zy6ekZczK4yjQ85oiays604r1lwP7WvxC/nNb+Uqkr3bqKmzFW3Mvlq1KakyB+oIfLZdXb8moaeOQ8EdzefESaINl6RojWUVpSMGWmvGEUbivrDG5WHiMuu7fsxg12v5EfyjbE6X+f4AtYNhcyczlLCXcwH/HfBbrl/wCvwVCB37+79Fa9xXwWBYMf2hMGEpJtk170SWjX6C/2KcukrOV1swboDrK6/nGZgD9BlhPb09vQSaKu7PZ09vSipXyz2lPZ0QBanRuCWD5xgzR6h4aOHeezphldmYmWvtom0h5wCxEmjh3mGG857SntqK0rsz3s8ckB3ntKN0js/UoJSYiVUb4USzeGdcAUF0ResyLXeqYKuQMqvXl7LTeUlkBsk6fTsyZ2cMN1OQ99pvmIYAnW95zuTE5neervKREGn1LZlRYgH+krCWNckfGFCP5OG/aAAbeSvgooBlj+hUb9LYHqWWfUodyk0T0l3au+MDFdY7ItRfy+njftO1A/mHjzzQ+H738sUcjd7W3rtCvBHxkLlevVynSBZ5nU/adouGKxz+CXFz+CPj5Q+A6yh9p55PUh9D3nXlNSdfaAlVIlQKTch+hfha0WFHWBE0rHmaxBnsXLtP7EbYIVv9ZlbRn8Sui3PSMwAW2zLRVKtD4Ch6iGy2Zy/UlKOgJwCi2e4TOKhX22/wC8rR3h9k7TPo8PLzG+srLK/VeplxRuebJWE5+kAc7DtlZKr/VAgOtcMxcU/M2JStsX0zP9RL54Kqlpmh/cILudI6yhXWnAT3CLY9MD6e1NNSjkgDv19IQjIjXVkKVGJprsZa2aKgGxvLfeJgavUhDuFQLdd4wSyyN5shQ8N9oUkBvEF7bfUxSBhlmdQ3CYN0JszfkP0O8vuf7IsSwPTn+4gWEDXLh+Oph2CXCAhqsV++33x2vYVOkNPLh5AYXp65Nw+UJw6Ej5btfpUqT4FV10+vwLn3/5YyrHumdU7wbzHcYIdPP/ALJfDrUcJEj6E/bwbDjT1IVVrUEjQV6QGdlL8aQ5XwD0Iq/eZhp9CebRRVI/GxVrfiAR0ZarPf7tXn6CoEcMSpRgPVAktB0iV1d9Scxl7XZTL8swA1rL3KqU3H0Ga+WNyzUqKAwVLC9lINF6V9IXaTFEu7XjTeULiISs+QMXrVDb8Irhvq8On0RQMmqJHFsM1VmxQjgg/t7GlQV1uWL1qWuS1N26S54ZNJ21F1c/UQjWoOsb9hK8Mg1TD1lwBT9cQVhdv9wlA1a0Zf1FbGGKdTeB8w2XAwwA6tO8UDIapjEa8CuO0ro64ppJQDIcdEWhVpDupH5fqDfs6Zy7FzD4U7TP8MEuyNpoDzNK4Exqu4sNgEjQQE7uPWn6TOT1mH+shOmNF0pzydlz/kfc2lXw0/1WB9BW5eIvF5ZG7tMv3WDZL2mQNVM/E6Ua4tDFw/Qkf+n5+CjR5TrBCgo8LPS+KL0n8yriVoQuHOtSudWjl4mWpGveFE0ySoIcJcyvZQi1NfHeY2+DQ+CdGft7w0+QvgwM9dCZTLWofC7o9ZR3+HrEEd5fxUNIvv8AJqcs1DmbfXHNNe+5xBCx206A2fLE2bvkwW7vJlMgtThCA/mh/LwYnGJtxXN/uZhwaMO4iNtzXurUDnoxrvL1OYZ++IxyN6vWiZxdWco/3A5fvBz92KHKBfaHhcq5ZuyMjpAlb+rcxWcw+M49+PBV1I/KjGhmtfDjUOXVsTpoajo3yxcmCjx85QzcfRCa03Hqe4QT2ZNlbr2n2SG/EC1qexJ7EnsyeyJ7ahVmOjfh96xqbgVV30nsyP09wIx0GHlqCJY+LmJ3antSeyp7cnsiezIJ85hsq88zO6quR0ZnLdlas3JiBOR3o2Z+kRi2nukt1sKzXMfwR961Qf8Ae+0+w1BQ0+i+xmVjExa401MQSbBL6iYiqdwgmGeLVgXW5X2KVy3BwKd8MPm0KH6sn4O6npfAzniDZenjXaSZMBDs7gpiPAfKYCUf+qGH9sD+iLSBE2Z1GE2fKF/x8QYXmYwqPpHw28ZfA6bpLv2mYafItqSN9u9u/CP9nPwKY+yCw1rQCHSdYhlQS1MkrwufZS2azLR0rZ94RrpfTbPXxuLEmFeWt/1KO/Fv7o9qyvul/KXXXoS9lzvKo+TvDicKFJ0HwSrxWlkJpHCtZ7bPa5otlUNSH+XPZZblVqEzX9rwMJzdIVLwEqAAsG9JUqGls0snW/eGLh0w3CURy/hmimUWbT2+ezwNqGrGhPZZ7ZHOQ0K0ns8pTPNSvmu3QKvaU/ZYuOWX/c18cAz/AHiAyrdVFt5nhzFozFHAWcIeFy/BPD+lPPFvGTVurl5Sbjn/AHr8xXzWZsrpFfsT5o2tFcZ4gbrfxP2nHzqgKIGp+9ZiNBNe0pia6rujb6jXrSnAY3ZRrCn7/wAYlXwY2ruTQAC2fhlxClCLJw1jGYvUeIvSC85eZvg7qDOdC44c6bnmJzWLZcpalVI7Hk6+UADL/T1+d18Z9pXx0+0PkkgfjYmiakLOUOcCnkAcb1hHRQdE5UrOTWZblTa87BS27thFaTMXZHI9SG8bN/dd0TUScXTvAoZ6uw/n5UHQP8Up/RB8r8B/4W185ui06xDCFvkmCexWpLiF8BNSskKSt1U3CYt6b/Zlw7bf0FSmcfNaM+0j9fO0xN/e3T4Mw9GwTESurSyKzgq7uJizSHQ1+frTzXIy3V5XWV4U7iptqf7rK7o5y71FJOpu9OaD20FUlMB13MwylutdLIbhNu2YppY9ajEGibLKNeumBJoC2gyzRKq18C5mBDfHTPV72MfRSCwrpVBDp8rFzhrT7zQTi6r+YZ60F6XCmsPDErGVnVMd3Vra87xjjUDaH5Onq/QpPBv2nMPgGn+tIR0P2sllsBeCHvM/VY+5z9Vh7jP02LDoDav0tjKygQR/v358FwO2AfsAN7T91n6rP12frs/ZZ+2xOOD0+fUDejVjmaZjRgd0C31sS8NfsIiBZ9RaQp1Hdh1FrLk5GGUB/gAj+ImkHaRVaz70guCuOrekpOGlHW+ZaKDGsw7IWab68woKZXqxHrXDJfz2XT3/AAbh4pesfmivifNB6TQjRz0WpDtMHF/4KDA31AG47M1BpcODtNqWZnZ0EGZF0OX68sWqdfWx2i7Py/PJ+O2JlX5/Bc+BL9jbflfZkUEyCeqBxDxkAImGVXatDoSpZFi47pYbJSe2HEyC9agI3gakRk5bTqz7Sfd5aGBauhNbr5fegQjG0NapUGGeq8sf+/xnQtL2O0H5ygsvQw6zKHQxJl2u8yspkQ1xmVxzDUyRAXpCNapm1F7/AIbNOJhG4v4i4cDDr0BNuU1DYiu8ARHrdRmYd0K/mKRMRWu8uJ9vrLwatbqnT0DdQKPsRU39/wCSGh2ylbhHUS/rP06qZgtb1TSNh/MzH+qrnaxxMe70vSH0H36M/ac+NNH9aeH7duStHDqXi/iPc753EzTS85dg3P3/AF8N/gKf96/PgNdtKvSpdvhvdp+lRBWn0dRt7202/wBwx6hByytx+Us3/n+sEzyyhLdximBi7hJWiUbVo5Mrj9XB+Ixs/P8AUjr7fyf3LXB0u7KTte+aXaDy+gZ5hH5fAxQGPjgQERNEgALOH4I1fACAHeeyJdVqRVI8yv6J8sdtGqtvwV47IWQBtADy+BXXvtMTozPT5NXzey1pDRDOpuYVOXucQwZpzesPBg1bnT1Ork8pNL6upgeJVdpa8jkri5o46l9scFeta/CVj3v5YDvdcYftoGg994fMqBNl3NTJdFxFqXF9k6X0gWhFNQiJuog4SYqoE2XdotqEomCqgDdfTwobo8EOpADSIikJiKagzofSKahKpVT2r6L794ftOfHDw/ekqfvuSXBFA7xj2Crx1Jyekz2hlf4GewMOR6S/i1K8bT9n5mkdUDwPXz35lsU2tWm3pPZGeyM9gZ7YxgX9LocG6M+CCyaS2qmnp2tIq8nnaj2FCrT6uEzXqD+pjlchWbJU6fKwzK+Oz5af7IweAb77+NToI8lERRKTwotfVE7S35e1BszVWq6d5kgeLOiY+GpaXxFCxrIrbIch0zjWxsQ8cgZ1Y2wlrlcBze63bE0zju2vaV5guh0kvbYwp7KbpL8EB49Vuw8WYfnXk+StLP0Fs9jT2FPZU9jT2pPbk9nf3PZU9pT2NPb39z2FPYU9rf3PY09jT2lPbU9hT2lPaU9pRY29xj/2vv0Y/wBTeOBQzF/WnhT9fUlwMIwXr4I68+p8Gb/qXguD/X5iSsoX4HPqPzMz7ZNHWXV9fhd/c8IIIjRLPpagNK7kZPWqA+BYENgLzAa7MB8pq64RaNuogydXbSF1jSac9fMo+Ugt884cxrlfmHiw9XHk/wBy5crV02g3m9pDVTiZtoLPOK7ooepLW7KnpCG6C4U03QdR1I/06JRc4XTrySnQoSrflnzrwwS9wHLI2MHYUeB/3ShI4q+DofffacBKP5+U1BJZGloLYdMreVMeFy5iYmJZ4mPCyWS5iYln/tfdo6z9pzL7Wo1Gk9zwKaOPSVKfr6kWUb+C5QAqtAbwN8/bXaV/X3jPs4SM+54ZKrV2dYfUfmYn2aehkSngv4Ln6Tj5lzOKjaXjaPJaSnKXnwUrVU8iHLNWXcM0jqlan5I5js4XzDhK/ESArMn8eDUs7dlzrT680vsFTQdBa9+3i/GHY2ayphx6faWLaPAlT3xp3DNxa90UrZ71Fp8pgKcslKsFnwAFZ/rNqfyHM2YwmE4kuNsO7felT0nuVAECDOnaccymK3Y0DiHIICtpUE0jvyEuCO22rFp73oh0Claa6ymu3AGgGxAcKNW0qY+nWgYvUXBuFR9IWnwDMuYEfiaTBHysjY4+8G3pqqEaFSF6V5TjZm6yJ9UszANhww2fRc6QYInv3NMWnW+z0iYqUcrslKadau6w/aBy5vtFxXP/AHJnJtiFPHrTWNQKIpfn56Wl1E+pbzWYR+KZN/Gre8ts3XpLrVsIjQom8qIbxbOkP/ZvIqXVRL9/oi2DU0s9jz2fL7RLv8Ca3h4LrNNLYA4nWeidb6J1nonUeidT6PDXaMmKrGwz9IlMMcHTDwOxd0/UYfAcbVLG4nSaiJ2jLFOo9E6z0T9wnV+idR6YCHYCu3zEHaZ9w07TSIh1HouX2xefFT9BxCqn67iKZ+3czVPq/dYYD3ZorcuukAyt6jNnEpoSlwvmQY+4Drcs/uY/AtpdiTVzPvQYyz2XcBvQFqsf9EVrWxDQaaWadrlfL4V5Oidm0P60+F/i8p/yft5Wfnmevv8AlgnwbkymqVbz/wCfLDV3dngguG0/nPPowkU9ZeVA6O0wCUNiAIK1/eoXyFA86iKrQTdylN2s1iZ7zrhJUOGwQoSl3eVkLyGnCGlFqveHSYRFPFgM5rjFAZF2eZioVkPWGPQBcvQjRCdbmapxu9naGGwpyP8A2mXQtJtc9lj22H/Lj2uPa49hj2uPY49ph/yY9vIf5ce0x7XHtce3x7fHtce1x7fHs/gc9jj2GPa49rj2mPYSe3x7HAcMHp8xhqvvmsWrwZg0Bp/jHJw33QM/acQGofR/ifu5tFcADzh4Belq8F6kaItqXvfhYF5jwpgaJeAhGJYZvKjUCD5mkfGPulDH1u8r5iQh8vV/2LZh/TwaIgOtzTyn3jRdpo8PfJpz7PzBOyaBrKOGpsd0onSYj1IOfBiafeX+Q/6pH/OVIkR7E9UCmivzFeDXDtiGiA9hvIAnfRPxkpv6dqXcC+piO0qAZHPlA9GfMv8ATLKdB6ckIlC9EqM7QC+CA7+4Uu1y2uOLGb0VJQsfqcYQFS1jROKns3GYGErja2YIY83NZV+pXOnMSF8twTBicaDyR26sfNCEqZjarDaTWO1ABFux6/SesxigApAcAlVTajAr94IN5hrQ8PKgfdW8xvLDb5bKZtE90uwUhSK/SMuUazEHlNIFjzn6TiYIvT/icL1feB1oYaTEusPrT4VdyGKucl9I6B/QSOu/1aqVDMlm8qUvrPPjeWDDWpRxhUVQCqBWYStk9Pf5w02dM1NvGz9bwbJUXT6PWAUGeC9iEwGoftEuXGYvB7Mt/UF5MV8ZJXyahfpME1J79R4L5MDA89ZdEWLFLYQmejx4Zb/Cczzyejj6KlMcrUqfOS4ishydIpT0G8MEQL+yOhTsOktsukuBiYtZahQmXVrUYCBquJs7C72h4SOif8Ai1Ij3Jci/zilvtHhZT6mlUxXkcO2CVORV3DsmEQ3roqC/pa4tyPE7ipd2zH5s4LqerHF9ftxpMT5RFjm/Dlgrm+6SincmnnpFeaPtl9H39JqO3JSqQZby9kYpqLU+SI85cEVXoHLM48DoZMNfYxsyVF02iNDShXUd0CVAINfMcVL9fSWnBETPzIMrNHZXMccXBc+sBDFdeznBweaulQMOWn2c9MCvl6ATssX+TSf65H/UQmG1Al+smIfpOIVUV9v+IlbbejeCIsMDlQI+cXk7w4YUBnuYiVEU1zMgmgtgYBf2bIhM6R2r+hU/ZTfzLisMDzGOdUM7s94Qc55QY9/g9RMwfm1LboydSa+d/Af1KGc3mkdEwnOZTjoI8jKQw+7wS6lQ3uMGyampK/3qS/etsJ/JSvzNWX1fie7ZoH2027JgvlH+5o95pDLBquCMlbrW0fB2E9HwN+KkY9x/RZcn3DNSJWn5+j3jX80sVj/tIz1k/qmHtq78OjHJXeMBFlxzcXGZ2G7kzML76HeYPOqRtFndSO8/oltF6r8v+DfCBqs9gwYDjVpi4nTHUT2LBhAk9VQ/zc9pwUnbAWKDhutE9mzbwORq4m1HPcnSuQEQpHklaKtDTMQ/oz2rK8TkblwLwBPbs9qz2nDr5oA+fqGkxoENs97yeNU9FNbQoleWYQhr+DwUaLomRNQ1q8RVDP62idd0KfeLUq9duyVMCc2pAEDQR18GNjXwRli8dQmRyzMqcd5cqqw1UPD1fAiBhKYRFujBJltVBrW/z9M57nRmWf8AUKNZU06H7t0GiCqjxewA00uaCzL5SuVa6I0rBekwyjwYiROALWPd+Q6MITH+sy03bQ8/WXMpjxMtfq3LlmVvnf5M6G+eAADb6Okw45awMC80S6jRy3Ld2k0OrvdDGQizLcUt7rG8cyp1aPrslaFwFXyzD6IN1RMdea73xLkrxeZOx7nUq5X/AAQ8gmjozVVUZxdy9pogoHLP7bxGqq6+803xAcl5f2ExK3UvQ3pBWWkjVVaHMGPIM2ol6TGsSnYgNcLyLhlqtNO6DhZdyI3c56SuMtGualYmuIGg/lBIboAhrkqH85cp5HWLCWjGKRaYQgixRKapXSWVrmahi4mHY84k1NqLbLBTa4pnTWZBHAeV7x+FrT1MQ0+diFS5ZLmJcxMS5cxMSyXLJiYl+GJiYlksmJfz6lo0/ZZ+B5f7IcNNBMFjeXvM1lxwGVMdk1U7+cHKzX1zuAfnEwyheqBbFZbAZUEy0XMM0iZ/mYhqtl3Lf8R7Ypf72hsCixhvdN93lOm4Dfkj3Ja7r4SgtMpyn8/1Ar5wfNctIiFy+wiKypsm6D0FdwdIaFr6Vw5tjsPBOIsDxGoo1pgFSUkCrFHU3hHhm4o3maFSjT328CO9Vi71XTUbYoCVtrjBwB5JXMs+0hc0LWCELQY2YTe1PTtEeaw5X/3i2976LUVsmj6OtOyRsl0vntFyCY5pUepzpdAhYAUmiRnrVFVNCJLGMTAaEBgO23z1cwzAVhmVclOYHWjhIvhgplBD2jmXCWU2jU/oEX0jdzDItVZjOUGXnEiIIXpP2MrSUMa/d2JajQq2azvtjAgYXvctkpI6DfznSZ9HrH/Unvk98nuE6L1nuk94nuE90nuE98nvE9wnvE9wnvE94nuE9wnvk94nuk94nvk90g5Zl+hRXzZ3O0Vl548kuF967Mv8yVnwPX1/HibShEf3ivCEToAmtBOmYHuG36TS7QeUTulp3YcQzji5mRWS59vCr07G72Ii86yurtGju+3Z9A85UAdKbRFuQweYnRt8oQ6oEE+3gkDB0mmLN4RmlwhreoViexxXDfSbGiLdVejmYb3rrz6+B2Vt9UEBJ+jkO0wtW6hHrsLVWZC23fm/SALun3IdoC5X+MNaoPxmGQCRQ2EY1sCLP/eoYBVBjT4qGIJt1oL/APBE2lc5lGCOj4XOt4rUNA38S1K3V+GH6apY+Wfwm0Dv/JtKG3z3qh11AaQUqhbtPRQn4Dv5Q3bTDwfu169KiDLLuxCX+nX9KlsybW3zYZGtj6BgyjB1BraLJxWhe8O/gW1OksxVrOJ/MEVVst0mOEW023E1R1bN4aPSPuFmj0hDTZW6xfjpoxXeNj1HzwPPKp3RNmKL6TQVvKukwZ3MHkx51F3lQQbzHpNsmmPbD8/eF0gy9siwHodXEX+zKG1VNKM71/6W5zlh3tJaezv1E1k4hdsYaobhLdZni0Mtz0ix6r0jtCEnms848QA8jFyg0xajJNXf4pitEM9t2mQLDAuuCU25OqsJprNk16TXjKtX5RMuKXTqS9RVv+jxEurWj6QJ2kA15R4NLbU6xZqbXr2YDcYLW+mIdZevn+npYuX2m/K5Cf4Ov8ptt5jPbybF/Saxnr/TwuuHOtvsStTrseggkzwFfT9TZ3zo/K6Tz0qcHh+iQFmRR8GOZ4fDynO6rh85pjiGGT+3qPKGS6CjdUcGH06YgwB+CJeO1L3NiCqmzCJyhEWV1ZSOItrgjr+hQv8A6k4GKbnaHcnANdB9V2REeV4R6bf1o7d0S3S/s2hqjmZuYPDTmP3cg0reZhhB0gcBzupMMYhxWXmmrpVc5Zv1F+yGDA7HPET6Y+YvsoRwSV5D12GG+WJtuiPnJQcSghwDXkmqF93Q5lN5A4fqrNpqV8k9lzSR2MA0LylfU0Mair0gTwuX1ii2fUC0WXGs3F1VUYzHdvv090gziRcqhtMzJ3NuiDTCuH8wTNdrC6YzVnleql/HEtY8+Fkx0sxk9d9Y1o+dNusu/of9RlGslnjUomJZ41MSjwx8VfBX/sOY6yLyjyjtK7Zx5TU4rwwy3h0TgIi2bx19INWDXmkHI6O26+EjdpndWmS4c7sEM3zOETgw4YZ2ScYD4cHEZ96808p1WAieYvowxZKgg2L3mlf9MzLA4SuJyr7pIS1ZNBNwMBppma4qL0JZ2aax7IcFGa9hV6IS1QDcEdolo/P5BLYS1o/LpfJrWZVjikLQAtbxBCeWeYGXuLNv5S0TGNjvLVPa5XSUw/cGme9lcbgVuPtNEtwrVNOaeuJ1qStFmUhI8kIMMkbJ/wDLXWHVGns75gNpbYwjpcds21g4yztw3ZNYSLrUXk5b+JosjaMbzKr9+EQ+pHeh4JWe+gEZ2mwetQKtpAt3uWP2l3lxC6I1cQ4a1+RGHstg85imVd9T+5CfQXu75JKj9WTvNJsBKZ5wtwvZM1DHF6xi+OdFI7Zn6F0xAndxikEVV6G3/wAur4q+Gvk1/wDoLH/4Zl//ADn/xAAqEAEAAgEDBAIBBAMBAQAAAAABABEhECAxMEFRYXGBQJGhsfDB0fHhUP/aAAgBAQABPxCVpxpWhzuXcO56eZe06B170YNaLrW2oG29MbM6d4aVKrQuXL0N9Oy3aVvOhjoF9K+g7b1zKdmdcaZ0p2Y0ZfQegGt9OugaXHR6feOtzOhoGjsPxsaGda35mYEzsNmekbM9Yjo7DbXSOhzobDpHRrUlbr3Y0JnayzbehuOo9W+mamj+ESuhfUvQl6uhtvZfUvY7A6VkvZe2+kS9M7L3P4lbK1z0r1z0c63tYbDV6GWGtdLMzuvTOt61obGHQzuroZ1IldDO125mNl7cS3a626Xpna68dQmN2NB6hpmHQL21uOkfkZ/INLldatxvrSvyyo63sd51B1NtmwmOlxsqVCU6Y0rTMJmW6OtdGulX4F9DGhselWudOOiaXv41dLYVpe69e24Ze69vG4jpe53Y2DsNh0K3YhvrW4a/XV+9CPQzqTEZWx38S5b1q6N63ux+WTPQvZjfnZjoY0xodB/AvStuJfUJXQHTG92V0Q0rSnW9DoX+CdBOt9Q6Tuvofeh1C5cvR1PwHc78u+5eh0l6IX0qevXQxpWypUyah+DmN9N/E52Z2Wb8dC9K6ONfro1tGujXVz0g3WzH4eNcbMbMbyZeqRrZxpWt7wNa2u2uvnf22X+Few2U7g295ehMdMmek9EN+fwE2Y2Z0vS3djW/wu/SNzqR0vUOvnT66WYbb631rUN2egNaA9c2Gh0fvYfi1q1076la/etStpb0cdI0r/4Rq6Z28biVsx0TXJrex0zobTRN47XoGy63LtrR2kNGY3j0KTdW3HRplbK6GIdA2O02V0HX7651K3Jqe9K9zOtfiHQxEly9uPPQNCiPWqO7jSnZjoL1q0OunXrQ0a6NSna9AdDpVoTG6+vjp1pmXsTZfVrWtuP/AIT/APYK/wDgXpW3G02czH4AR2Y31sztv8M2m29pK/ACPPUvr50zpnpU7MulTH4taL+Kun1K346fG6tt7w6nO2+ua3AZmV08fhL+RSfgvRrc9a9uekSt16X0V6AStL6xobQ1TS+pxsNlQ1wbiPQJxtNt6XvNDXOhoaVWl6MHW9t7+2lO29zuvqE43VvJxpmONEYarvJeuOjnQJjcbPv8DMHoFa46BHYFx2XpjXmU6FaXqkxu41vTtsrS41pe63Q/AvV3GtR2JDcaOy9MbF0vS9mJW7jU240xMaGIb0l6H/wLmJx0s9TP5F7D8CvwSV0Mb6h1L2vRv81roGz73kuX060p241rp26XKZbqaV0ca40x+XjeSzoGy7l6X+EvQqVrW29lVtxrneSpXSt1N9Oh18760xMbK6d773VqbA21oS9L30/g3qhsztvbe2uub+Nt7r3V0sR28br6eNtP4F9GndehHGYUFWr4A5Zg0qbFDnNCdtBCsTu7yuxxTO+axBaDA4RyOn1sPwB6ngLyNvi53ueIN7ZDjIQyRaHYbarKzDqgKMbdk/og7ONi7MTGytSp8dGvzr0zv5/PNb6GNtR21K3YlTiWb7hpWy5nS3WyY4/aM3xcsIZCjhETsjkYT7uuxVvvCCBEDDeEGixzSlyPcV+/EvOBaHAFDs8xA1DygTkeKZnvNC93wHdgtoHIaHyskDp46JL3VCqpalASz7QcE8viHghygBBtrvVRFtTLXtPoRVXmtf1E7hLuM8IHVlbJmfs6hAAIVqHMVKiwzfCQAnLxVfggi3sZPshpiZ1rfmXjdeztpW0NMfj1rfUI6HXNL1xLjsNcdDMPwsS+uaMwxCvG3dOLImCFLrHTY5Ig3ruVWeHEPahQo7a4YcrG0ceB5WJBdpNx5Uvj3ASoOsdKgM9qhWldydWB3WF5IeQ4OZY4qp4OF2GY2DXsHIPDL6vMNG+jhF3utFoy1bKIt3kB9d4hbAkr9Qq3Zs/ToEAp/v8A44FGrhxAZ2c8KYinoFd1yBOZXHNoMeYVsmxyPeXWeqFzFxHlT/zgYyBxweOysrx7htvkiLz6srV3Iw6GIw2U9C5mGdDa6VozHSzD8MOk7MbM6H4BDpvTxtNaOqV1FG54wQOsCxmbw5Qe8Rlv9voxPyAigUGYFSsB4SrPaUrrJieCkP0RuztKqR3+MQNVwaeinwvMAaEWFzfoEvNg2ip74Fl8fS55gGAKnesq7nL2Mump5HkTkdT8TJEnMVx8gAdmoeJ9XB7nKlM+c+SwTJkxc8CZ41MpnhhmziIA2MZ/XCg8510uUt3WKTq6KDrqgc80jEzbHeyYrQuyseTlUnalOeJWXXRZVEy0CdniLIIReFftAg/t4B7WUVViq0HxDYmy9q6G/MHWkt8LyfyLMT9YOkuG+9SEH10zwk4GSDcrXMqvwyXq4NTgAHdjy4gBlYO4Yy2ygDuxJL0Qqy70rSthq7a2VsNlbK0xvz1Odb250HZW88pQO1Ep9IzD6PXfA+UeYuE8zHmT2amQm5eC+FwUiDRYVQMn7106y9+TzGrwCrRzKbiPQVChHIMvEBCi4at7IebS4EbMvmV+hAW+WSUDcixmQlYo68qeVWvWrdV6+2o9Fi2/u8S3RYqjwu1x8Q3kRPfznsjovF/c4p/aolmdRFZmnA25+uayXUgVHeajM5X2r3Xah6rpUfSwgo0tQWTo/HzJTBLHnNmfFH47LUG+5V8MEmLB6XxielqcOStsIFlOBDHoyi2vPU7n8yH1IPE9mVMbb/ANMjKAH2x8rdm/s41UHur+1UVBTlJTe2eX8RWP/QoLh+Kbz7eDDcHaf5kyR/JA6PvCN/fUfJyaHReiS9K0uBLbQ9JUyaKH4bUDvhU8HAlRl6PmIsql+pZXKt/bko5/Dzpjfex0xuXUhodJ1rQlbKegxi2jb19oBt2QWIMC4UKDXDHtsSY/A33jxa7spmntJSYvdc4LSz11dC6WHbsSizyGjoDyimlbeJKBOAQO72Cji/EdyYsLA+L0EqWkvfe29hpjSocitIawKZaKz5t3DJN0JfyYtV5gb0hg88lvv7e+crdk0eTMk7XeDxcA7sxUXz/MWWZS25M/aticuvLv3dO6N3fLX9mZZs4X6qBw78xHtlw8pzV6yJfFLqPoR7xdo/OxXdhL3K3TzTsIMxcbAezDSvYeQXFwrUN61lm931relQHbWigPbHTXaO2/zA12Z/pYA2XtPqAJVwFEGPhi5sE4bXoED7v3rLzXGHEAA5LlLDB0kIATuNkZiidtfVI6AMjB+jOMLilf6TQf/B8SDLNt9JNMQlOI/wBXsETAlg4Hj5g6GANOuXwviYKNG+lZYa7+KpAJgWrf35EtSmDfBHyGYqWMf7IwgIqAFq9iW7j/AKfBBQjA4RyJK6R0iXGVrz+Lew1rpUamzA14j4IHumNicjwYuE2BflPBHuoxLRiBQVmvlxs+1zgTC8stssRkI47i7zNeFcNQUZ3UcwqGJy/KjB7YxKFpy6PcNANClgrXZAKSd9mdb2u29DSmXCcVQfPGEvHMMUnApVr/AHze2lmZfgxAuevOlypBc7C9IPPLCw/T4+b59TJ58ZvTxiLlyiXOC4VXWIjFTGFzDLvoQg3Kt6B7MBpny+NCFA5YvwxpAWe2HlNW6LkF2CM7lULaX1q04gxQ9yxt44GT/Zw0lV3BMEuN4HDlOyceQB7jML3EqLqJYOaLl9NAwoEsqoR/mX9JF8IQBKJRl232lft7szOALEMs7uKJlqWANDJ2SwI7MZ9LvC5jtRf4jvgAkqV76F9Bgkw5P8kDorWff/SQQf2pj7e4pUNxar+VCbf3zAxnOXf3gRsq5XKwYnSfZYUnPk1fLwJY5HT5XLCJAT9FQ2AFqtAHdiDhxHn/AFhUcDacwGgAAFAGw/CxuzrjY7K2PSNHUjounG/5lxBrBfCyOvxKQO0LsYwQHOEauYX8Ww6Uca1mFjlWDYyI8Vlnllmq3kfJd+2C7pxpxX3u0vQmhP8AvBhZbxVwFcHaKhVBOQcb3LgglyuhmGmNadM7LYplz/WQsRJs7RCpPfgFARFLgLEeyS+6FCmVHu0WQv6qmRmWnKuU7rMpRoPeP8GSh7r+IPXwkj4MfrZEKhLuUQPyoKxHsx6TLG18D5UOuj9HdC7sbq4zs/L7EyR2WL7o5FZz+eHjkp6Lj84nRuK60yotRdr+z8nmAa7C9wnO9dCnMg0H6YfGSplSZICyUpPnEmz718pLXvJCjyWUSJ2tqeBcBTQfvTP2OtBcqPrraq+RYPODQwRgLPzgIAyqE5kz6Fwcp4CNlHofwJW2VDfse5CP9rn8S95PnJaxGDL3Y6VS2n+sPkiN1eTxT/ZOJvFOPX2hdFQ9YM5mLbyDhi8W3LcCwrkTROiXtICP9WqAH5v3wM26qoAhcE1wMHsie9QMACgOAJnZxqOpHUhtNb33uvXMelf4V61GOYcGcYAew3Bx0sX8Ufu04mOHCFLh7e8GGjx/ihiHDaoENjTT8r3YEvc6rdWs8TNpZD+rGEpH4qIoSjfHlGyKevxUwNx1SXo8GE4p0vC9DHkYCLOISUrHFsHJUQJfI+wgbrYv6jLr3vmN5byxzqtMYhe+AcwWqnZkYLKSv2JEz9OfSrH7rMATMFIAC0jhGLWquWDle5EuhByxNMe87hJ8IQVUtm1Zg9BKlzveMGZnqwczMtlytLg7saYRSuVk5U/lNdYVTPP+ZtDn201ZcOCtXZFSZNh3tJ3TnEz0Y0oo3EK5kWU4zz5wKJ26AXF49yv/AHkTqMcOFiviDYRiq0NXnQGQUlWH/UgcB14CJQuHu26hRgwUfUf6ZcX7Pi712ue4cH2IzZdfE/vzA/GLWI/ggqAHKy/0+rY138Ll+YS/s+PIR68ON/EDFRPtjEIM31nQn7c/DvBZTxrUK8wzNHdRbrVfQ4EWmde1Jm18d7i38/WDt8Q+QAOgh6J6L+yg9Dj8DG+8bjeaExp23Xpe92VqsuXji78JmyUNW1Y9g8wpxpp4rKGVvtY2YYyHwRIq/wBqOtPOs0VzKhlwMC2QcOU6chR6wAAFBgJfUxpnfdRFcxW7vYJJi0tsBmBS1pCpwIoU06RYEeCWLX0/ql88sxhjQjQFqtAHdllXDx/D4JnKVQtNd8/0MQhV5LOw1wzD/P3du7l30YB28vhl1oAYydR4vZ+Hhh8Xh8IT4YHU5Xc/EvWulK4ZwUOKsdYzsvZW5QIdAoeL5yiG3LJ7q94KsbzqeXwRFmClRC243cFRQl6AfKr4jItzCKv4MOtUciFW+2WjD7PgEpX4q/4JQsrsctK0+TF8v6qI25/epmKceAMqDvBvB13iYx+JUX4zUNfDBoRyNLuH5Zc5wTjxLLscvNIAmUKlHc8TAStyXwREifgL4CSuqR6N61qpGDC4n70YInBydh4YgVVfeyofv9J2T0y3B1tyFyleL5CVx+rH/uRjUH9Lki0c1FAOO/KxH5DyGtFVfsr1HLWXWljlgtCI+RJhM0e9+Fg4lujqdHPTpidMOuaPSt0rQ1c/g/lWJXAB/OlxUDyb5sMNv8SWg0bYB6wg9sQPKpD944xsAfnIgNc/VK6KOjXQXZ6w5yShVjMOZNFMpmY12lQA4VO9h4U7DsdkIWgA8BoxDtHlR3ebjv8AeeYyOqCGEMvyPg9EKk0juMeZ5Ho8PsmTTT5vl8kBwIB3HTklUZwqueOBJxjkloeZHmbHsYjsma9qTrBHpicmehcxsEtxu7tCLC8DomjnMXiNFZAACotiRCM18N5Q8lp2qfJ3i4f0f6BEi8V8xzLEUq+V2XrcVg8w8uxvP51/n3ifDlFqVAkvKgraP96i7DuwqwdAoAXX1OTnpOFjEiAF/kP0xNHGXPnL3AjvzpcJcxKiMM8VJZ4nJS2+llcQFp7+0ddKWuTJFvE+RsgC3MvzfRFVhopz7McaThEa2Afcoy47PpX7xWzHWJWlvSZW82H5NbM3CwwDnpEg4uLvWr6Eb+i7+ePGgPgITi6q7pA1DPHyZKap2/0IG7jrjAQ4Bf0hWy+fOOCTwD8CoXyNznx5kb/XctT/AL6H2v6EczOGeIrcCD6S8z82KhgBVOmFtDB41hiAlKA5VhUQnn+BKSUQU6pff7QleoMdtkIRbRXaOecRa0AYK2g/eX+cBOQ3AGYEW1Fe+CYUS+EsnNQwrtV4ADYY/JcNMTHRFqi7HFkx5mG7BG/ECihOWRO6DBxEfNyKzPxd7RR0WRP7+BGFl8B+D0a1cIixGkYivDhv4i/1FKlDsk4RpxMIpIVyyjsM5bb6l4iiOPSA48ZwaHuj51XKmN6WbElxEPUVK8c7nuegULjNUFMPTCAAAoCZRcCyh/UieaCU9ZWLF801Hc0WmGj5Vjwpp8+SpZ2/Ir4YGGHAFfwwomPYwfLGrLB+PQhQS5ZgYbTU/CxvNl9E21F0Z9bq6BmWqf0YgIFKawWoXth+MlhUoop3g/hALOJtPM5n2/0uPjw7CrADz5MIvbvqnkwLS1aYtUvrDClLxdDz8aOla1renO42MUgojSCViMoGQ6CtFJHOtnYCLoiGovztvgyPqV2RommO/FYIISIWRKVFPDdFErSMG2FwoSyJMkdnzV9FSFbsDKgt4nOgsiA+f5xQTXH6oXOceNotIQyyAtcSkGbdy0q3bjUZxoxan+t5PoS7Plt5JVEvQnlhigL659/spl22kXdenzwI6h3k5fMeBc9MQo34YV4CWheqKWfFxK0vRJaoY7meEzyEfI05mvfzzpbLbLH6ZSJZdw9r9YcTErbjVnBSAW3UpX15MXz/AFX+crz5Skx6ovf0+oMJ+cpwhfITg/tJDgvLAS4LZTqUjPdBDnyq5RyXzAS/pPOeX4P4CA49D/OqM0b7Itun4ZYb7Si7KjzRfpWMLFpHJ3EwdDHQqVqErTGuX8LndnZfVZAWRfFhEC5DcJau3gDwTsUe8pmrGoRoJqCj6kqsEGLwWMTm2AFzhYMLSarCsFFI7LYzpdwkxsseDIl/gMFhru/sj4YnF+0cnZMg8PQvrMYg0fj/AJooVxII8x40jlmEs5/zSw03wBJRJyYiiz6JnGMWraOO+Dn3HPK797/DKTmWaIKi6OX0e2LyN+Efax5NV3C+1DFNEL0dyrBNPv8A40wieKMu/wBqMew/wRMU6N6LtFZKs/WcFCCA7BszAhruLwJ+i8YdvQStLgb1ArVewQ+q26B4f8JAt3YV/SZh7BNXyjFUAmJoUrX2ZwtwfxgWDBO3kmTyLz7EMpmjtR2O8n85URqM5Q2+cfb5IReiSz4Bvm3Fx4U+OIgdGodXzBcyS/qS+q/yxH38CQjq+VZP0pFKY9hFKuOwmAgWyqiyyV5e9xn6mLj7av6MGCt6ATsP2TQ6xIMOwVH8LOhGGmOhfUOq9JlsNFA8u56I2WsMh1yy2RCFplpSNgQ4htgD4yoheZQ96AZ4OOZaC6zWXHfzf3CvZHIdgty8CPEUIjRWqu9SNSy6veGDEqogD5A+7tGQ7h3hiNd6dHfbL1Nb0rVD3gLlpdRXL6pdMlqAjODppimEKBlqdsfBsRKJeoe/uMVbsH2jZCvKtsVQp3cuR/yS8AnqxT4IFWtV7eouKVFTxXe5iUKHsGGKwYpn9YyIv/nQVAWEvodS4DtupiWZCZ/5oupjfeiRocoPngQ+fe3024VL0VS6tq8XHA1V0QAGVWI6Cu4fuvKMjDISbukmK1WeLnc65wFsXB2hLAfAylfePdlfYM8/KhY7oWhjoSJG33pwfeB9MHMPP3cccyrsy9XymG7JPCDHw4Gty3d8ZUwxAqeP3MgbM6X0GNt7JZLNLPf/AIcS28GMPQbBLp10uo8U6j2v32MKXyP8wHVP5P1YGAAeDpvTejToaHQvbzvN+Nl7sR8VAyMHebAHpQrJBXgRf2RECqhU8e7swFodgboy/JhZ4KstZL+URRgEq+HDjOb8QtL2ObbKKibNyrtdf04QxFk/+hYJuGmLoMnnErD0hfvTh9fhkIDR4RIcyqP9Qi+CN+BcxGGB9shOA69meyAfc1J+qXox3mOtVMxuN7IgYMwNIBHLI4R5I8lFxRTh8IZoRzRV5uZXL2Vv9Eol1PBvwp/5S9/Rcm7eSUntOOpf3AWui+9XO/jQfESdrAQ3Gtx4edPUgiiH5y9FSo0gLpm11Z8Rd5lxgpV15IytFzarlZeLIql8vMoouyAKbpiy2opesBLP9dkKmnlD1JANg5DgVdFxIpnD7cT+oG+DKkSnFRumWF7McdfXIupUKIgzE4Yq+Mxj17i3HLvkLJiCBIHgdaQToo92uVAAly4VpXQrrmtvWzpelumdt41OhfQzFjd0B8Y/zw80o4lyw+yd5Q2OsU7AQ0r1EBGB9xq7mGi9qPyUMjAivo2dV8JY7kdlDhHAEA0H4cp9tixdqgJETOlx6YWJ3bxMWvdWH4RVHJfBKqHQz0caJ2jwF3mlaZkedL4eqJZsvCvj4gdq6Jj3hnU98YmfYyenMqEGWsfsihHFBAd1wEK3xnvEHtkoEsT2REMgFwjwNGZWhAJA5w7fPMJkltZCdTe9UDvJajz1dHEXLod4aKN9auiIx1KPiBzetqnPiPtOpUMK+oA92D0rJICStD4gYtgDiYoLwEQKmn5gNYU7L2U5IBDH+gR9vdGVnPtys+oITPuAAIjQE9kvXfBBMQ1o5CCtFBo59oydonoXL0SyU8j18GyCVx+umx1DabOZUF/h/wC5jW8ov3HbnALVYfPQXvkRnOdE8K3V1K6BvNSXM7L6ZtxB2YjM6fO2tpNxoFiR6qGbUvvcWUVlAjnF2IqBNDT/ADSMTy0KzIF4pZwA0Yfif0YlGQFqCxjiYuiYC66sMPaPEUSlTFod+0dllseY1wJVbOJelQqLt+tQ1U0TFxRxbYf0yQMa80MaIntzYf3i1sThS6VGEDJ+9/dxYg0CkPZLuxh4EFoECInIkL2PEFnzTlipdoMhmXpU4mfOl+Hl8RP3r9rrKLG3D21jowm8iyyLqtT7zCQekgG4MmF4/Xg1BY4RfqIJdF8XiOlWSJbis5jprl0G6GkKiIKLn/OnTFxFZXdkwzO7LrW+ZVzEDVX1hQZv0GESs+zJYJVkWXROsPACCNWhA3uVMRTFUKF/ceUB1WzPpXMeNcS2gflXCJ3e+raJUd17+JcoZo/2AmSLm3b+73kay5HCMe453eeCdmTH4umK4xow0vo3FsFNywshEdRiDNHMTyyVpWkp+SbRfixmW4Fr/hZQVSojME4mMBEpMMSBDwBpgjMsFMspLIaCGD9dgUxsGGlAxAKuIeTVoBlgkIEN4UGljNl8CxaQYB1aCCdUciRIGWO4iQgQHug/mLq4LQLEtEUvj6uhWFtZL0rCB0HygP3ngiWW1XQrqaY3I641ZW0NH4FFI5EgEqAoYA3QDggqxLJm5MCgVOIUU/Kx/uZUJCkbIilRkqBQ09yA7qS1ZZpcHV23K3Z2LE3iFm9gxmL9suNDr1Q7/RDagM9rjdY77H0kqPueBefVARgsfzBRV5teV9ESG8CmAW1Qp2IkeLCvsgs2SShxBGyUWCAyoMAZeJPNJ6vIzDTzZexB/wA5BRd3KWg4uyH4Wsze1EqFKFnNO0lmlupuuP06BVc/ThHDRZk+kfklEDjU0kBGZDIOfinky0YjURBDIB+8EUy8w7jJTmbn0EIAu7QiXeGWH3H6iE3kA/cYKeHVLjyGHFRIIQHjH65C2O1HZNK1qBe4dTMRqKE8gejBgwxfHcwnghejSWti+6uSUDXPaF39z81TAuU7a206VoQKYiOXuYK9kWveWAQdguO8rEW1Ha0thIBx6v3WPa1uHupGE7qLoARFxgtoTLt2lgvCTlNCNPUkGmDYtZecaFwmUp7uE4gH+3EPFz1xbEJkwux4luUkfYpGsmP0tKoZd4apQYWjE4iKDu4WyJYMj5OCPxZb9bg/Kj39rK0Kz7OTFPxoeAzAJH2iiAe59sQoq5/6vAWnP7yFw7gVv02mCwHsl8iwEKWvoVGmDH6+WEpXL5ga0t2Lcre6kDS9SysI01dQaKmWlqAPhi2obB8bm5dSWRMyUDGzoq8vgCxKQAsjQbu2PC32CzcozAwm79snAwreqcVFp3Q/6rb7ypMGDMaY2O2tl61KiROMmjt2MOUu/uxnjZmE0kPLqHGcQjUplBWkyYP/AAezFvPCq/kNLizMzKYup/Qu0BCpHcBLocx2C/gnZ3lz7Rf2zuWnYJRZocSq4WJZoNvPH5O/e+WYGyk2Xr6ymHvMJp2if8vkrVpLNkgFEa2iJnAKgMRSrKgu41Pk3P2hM9oGypZhyMeog4y4Blns8K8KRMZ5DNX3fROBIj4FRdqx/lKIXNf6XBg63F5RPRH7CJwTJpjZelR35lxQATxJvuQQlwSRBE9MeYN8oHxFCrdHOhoTMqWPdFyFkIXUPSUuFOevvhE7BIYOCekTstgqu24gqxSQwDwMDoPgIkgaMo7IQ7Z/nqIdoIA4CF8vJQ+UhYsUfrUxascNRH4wECmHYYh2pj/P4+kjXJvr5tGX2b5cC4Vhj/PssCegBViUb17aR4YRfmNa8M/bqAOGi3cexG+/vzGL9wednzniIdzn6YzCxCg2gj3/AKMaUt1yrmdmf+EQtho3/GDJCT7xm+xgqems/hKwd2xF7wFakz1Dew0Q+hQwo+azEtzncvsKfMOvfYo+TksMEcAYQYXIjgTUMNBZIz0kTBzMWI1IYN8rdwS1bIFha2u8oJe133rjYy4ly2OYf5PZCyNJw72SUQ/K4so+ddKh4S7rltLruBx64QLOy+2BLQq0AvhDHtfrf7Q7x+DguZfdtLs5XOQEnblHGp2GKe8+X2cIj8nc8ctVvGFykCrRO0Wl/KiKzOn2YDtw3wX+3wd4APhcu+VY2Mqi8r3X29IqYmGqHNf3RmHPqoeVBwg7BQSqJaahLRfEvj6CmMvMFRfsirjsGrYOEGu52xA/as9x3ZAXVf8ACfDEa7yIP0xNTvKr+xKCrQFrHgV0XHCHoga2hmv7afuT+cx6EDKgQ4slK97FC4Vc2EyHJKdgFBvhBDhB+GWMo0up/wBInDB+G4DYISyNAfggZcuUytL0uWZiW/PwqkinIF3AJera4rpB5EqDz/ATOgLh8CCJ8khVHqFNgFcjLYHJ4mVuJovlGEJC8LG/EztLr3aD3UAMo+UgWoEuPej8Bolr5o9Y5IIvaPZOBAX3/wBMYosWSfeAl1qtIeIOLy+ICrk4lZpU+wbgK4qeW932x8fTJ4ciOZlIdvUCFNM029mWtEf9JA0X4NgDEAXHOlAz/qo0S7LaO9PPM+8xrsYpoIwmveHT40BUAOVnB2wKPmpjtF2Cn5gE/wBUuUw83P2Vv+EE8zEQDByrRE3M40/nZOStmKNWQ/aXKr6R/lKfnoK7ruVT8Lg5J+042MBp/WDgI8JB0pyfgf5R0fTIeFp16gREeGXq3uvVdATd7pnvzAv+K2Af0Nk4DAs8422JJJ2mHlJrw9Q9zyRTsbpKkLdv/iY/TN1X+LcEsjq3MNBlP2Sjj3xfzIt/e4SKH60r0tWo3e5fucfjTHUmYA9c4ytHLIdS30lVVEy3MymdHQvoew/4Z/dYB0MS49Qz+iGtT0M2Ylh45rcEVAuKuxlcwOcuW4nyjRxHmSLqfKjB2tdIzhontF9giVQpCkYycPBn5FAh77M1R/ywLC5w3Sg2eLP3jCBoaXZs+Kz9VRYb0wxGk7bHX01jPem/5pu4Qurj3l8phHOa2FILuqSUqcMNRP25ZUCIxLHaOhZ36VRhwNsw90+0iVLhBeSKkb+23NPabhXn+SkJgLqfZg46CMbHzFsynfGkkU2PgyvlmQ4QSEzopa6LY22TSuSV45FQHuL86UpoGxwehg+P0Mq/0YrxWwmmYuWN3WcwrhUCUIILcHQRKIwcEAa4RuUiIO8KVyEv/wC/4qcUMAiRQyEU2zc4ziZucodiDf6Oga7eQE8RP+BjJ2yuA0PBGBLD/AMNF9MrirdgWspSSGpfb5ViUaxh0xwU6tGI1ftAHNHbv4mgn9Ey+/VxP8pl3CmlzoXJ19Km/JyJssYqVKqSVCLCKyY4RAsnl4MHwojuCyBXZ7z0+2JUS1Sf10A8Swloop8z+s8OtkQfi32jFhGLkS4sQEFqCfi8yVS41fCiLOXXZgsw+weDD5Zjpo6/KSoUpPAS46hTd1eHYECiNjh7RY+mFkwOSSs4mPFIzN/sfRTJ969ufbPAJQCSLtA/xyXmRBnXYCQH52mQyFS5epK0Xaf/ALvQKPP67SLGtDlpT5qyGQ2MBMFjXgFiOL/I9zxJBYACuvN+whfgJ8RQ2cPI7xbgJHDBoAwfGBpNadwGUtYVMy5bfOQ02s/3Au0b5mngeHlx4AIldvflcul7HBzuLDjQhLNXIb0rM43t1HKeCwLHbwfqKCxXeANkIlB8oiPiUM4IJZod/EPd+I5wgpf0SeOG59QiQiQPo2QhFLw+Ixn35ZDAohAZ3CeriA9RVIAxBHkAbItAHZ2w2XWG99xBwE1DV0zrctlsWmto2mRY0VGZ9sdstO6pCzBbV7+IGsCkatJM2tZYuJ7FAGTLP7tYOsHG+jvDJ3cKqeZFkFVGsW2qwwv0639mY6H81jQwARmGwg2xoGEAFy4FsthUU+Nzxkzg1CuSiUhZ5oy/frMAMZuFosKX9oRDRd3J3AhKlXpLHPMF28bkm0Q0GjAijXdYmshXfv3IQ9cKEFEDCdyggckO8q+KXCux5bIdapmKg0wcLFelw7qNfmTaiD7J/akzlazVlzvdO3s4yX7rS5ppvMXs4P3YG7lyBwIE3GXVcX7kGZuwygMNClezGyJ3JT/wJRKKv8ittwdK240bTKG3dpOCveOk5C2l5V6EgtHAKJ9l2QD+32sdkIlKR7nCLDbAaSplVepUZYVaQ3+SwjQdc+Sx3c8vTibY+TZfGLq1SoHZKzEaKyivMSmuK+exPLxQpOaPBAgUgqfKmPVIBG+GLBBjPrR40qHY4IjGcUF+C2bu9WJ/8JOzDjkV1G23M1H6M7R2i7Sq8TH3YMejOJKquCDDPAWGrISk/fJNXBxZVS5e357PMARyt380XbUSovgLjpSyp5gI+VCB3aSqVu7MBWIR1M8LLZxIvi4OXxhbIIj3GBjRWq0hSPcnIFJc/KkMT2KGZgQPfgX5qE7KtNJOaIDtIP18IRSmILUB3WGDad2XW/ZlcYTg2VZ2YtBalbRyktJSK+Aww0eOLEx1wQyz4FV81DStMaXtXDEJGkXWFMWNHvNlEQrVSPIjmjAGcqIZkKXicKBQY1qw4u0SQp4oErjs4ya+UMBuI4WtIW2CI+oAFHcKTcVZcC5qS+snjKcwQWMXcLzBo+HEATWrKntu5XlgpRSEVXVksBNBfw5juOKf1iz0RycfQ1tiqGbPy7nmI/0zjjQlHKMXYTIzrCi+f+RhGWV58BCNiX1ZsmBo6Wbq1nydf7s/fJGglkfsFK+AIDGPex+nh/5+Hcnqm4wBS/psqYESxO4xH9LmFw6ZZRLo7ZMCk+cyAKcArJH/AMfGHJk70YFFnqlTmZ3Y6beM/c4t0c0z2g/ULl3MEvZ5Epe5v/lSjlUp3WERjr6UcaatqriSpaqxCW58huErRb4OEr+eYF+Xv/bguZgxQ+9HMUe+TmJkIBrbUY241dTQ0OAhePJL5keNMzhP0GkNSpTFnMbW1oRH0kNz1D/hDPHTD64VimavTP4jfLRWZ916/oT5v7Mn261LSpiH7az8d2FGBF6FGmYqEy6ufxghAcfoLoLicPnZmod6YNCXI7W1QnLYVR0K9SNBiIcQIyODvxDMOJ4eGKjRuAJyoixi/aqtBBfIp+lEIrCpLUGlRBI0vHMuWsvxBjCF7t189WXuVuSUlXrwAY0/nKzK+n5EStd+Cf8AFQmjDwFRYXVxZcOIqcKZhYBPZcAAFEogeQBhpePZcKKrEBVNeKxBAFO4NBwEvepRD6BPDmCgADgIKSL7lwABVEraT2XP+ShIOPZcWsCdyH/jIAUBF342GlbJpl+YK0q9YSfvKKJhLy4ecQi0DFWR4FEGgvhlTKYwLK/9XjdvmIecI/3sxwYrgBohqWxJthUV9RjHHHMKSFJSiNX8Sg4IxNHQ6dbEl38INGOO0sHmVJA0NrFSfTFoccIFAZKw80MEWM5CVY/ib64t7OVUuZbtDDxO1ynYhrWjBJnpFrVFfUhZy71ONF6Aqx+pykdohEeySpZqcRpuVBb40r5WT8ltNY8qcb7lvsGDgqKD4zOZIP4FVLLCP9+DYEjGp3V3ZejIwA7lBlFXbsklbwZwJQ1FheL6UxNZ7be80Oq9zQpxGEmERXmFpRMRyfY5CiVo7Kl8+Z9MmNTPQslpPQrQH/qfvLv7H7yn+h+8f7N/Mf71/M/pH+YJIf2j/Mp/sfvP7p/nQwf3z+Y/1j+dPFH9T95/dP8AMH/ufvD+ofzP6J/mP9A/mf1j/M/tH+YDkXFB80yoG2vw3cbs7s6m1rfNgsRl00UZbwpGgjnqlpkXdx/2ke5IxB54e2CfeXzA+SJ/e5gUYkjYBEs1p/kQV7ZKXVVk1Hsg+WHth75dh+rh/wCyl39P4EufMXeuppeqy5co0sBL2BheYpQHtJiVy7DJ5FwkPO0yqg6WajU5jZEI0+LfAcMGo7BWyZnIsJneWVK+hcBExL47GWKpn71I1A58TA62vb/VDFa5jTgEoZoERHgkpnw3qxx3T+kkP4usi1VB+UjPTMwAQ6ruzKssvGLx7Yk6/A984EjzLht88PTpM/XBJ6tvDhuG31y8KQiTBh6O6+glaI3ye7qsczDI8vAlXbR6g3FalytbiEQ5iIzvrInogmksDKwp9TCSkoxpzDC5dqlDLIhVy+yCT3z3ykXulguDsdDTMxsxs7aGOvjpZ1t0xq6krbaHYV+Yxl07OlMSfHHe4E1uggAFxz1XDvBWVMkv5hPrgLU9glCBB/Rhj+9mCo0wB1DuLEOgYdWwsSFmwsRHxyYChY4ndAWVcCoAT5jv+phpiGxdrDuXYxOEWmKdCEAYUidn2IjHlsz8mQ+UiwN/GBr5MQJfiZ17i/loalfJ/ddyXiXhBdMs9qQCk+Fxdt35WDy4IkuH+HP1LBI8yVEaEcqNVg1kEbF47iKdIr/aDz2UTHfy3C3OyhAo6IxFd5QP0EBCIh4dVuYqIPkew9kJq7X2OyIspPPfsxvOZObxfYgf2NlH3ZLC2rlLe6g/Nr6uB5xLMMMAuBFKE3LwhABl078DA1qpmu0I/RhFaVBSJZmODyJWAIwfDQUIfqvwhEi7e3yhJVkQ7W9oZgRvSw1zIlQiCX0H55cGBoZZ5e7sXW5ejAMeVU0wVmKlDy3K/oFopBotJMlHe4LZta4eFBswGClDbStki7SNKjkmvFRqrpLr8E4FgfJECBKyoXSgIli3gFhue1FBiQNcBvExGprL8MkVOAI0kIg1tvGXOJzz9BYMC2wMKiwaCWyC6KhBmadLm2VHy1e/SXmW6G/dTFSfr2GnnE4ba3Y6efxLrbjQ33PsrYAtxmoVF+ORuAzKJgndMkahXhfpjfzUJqHZSvWCSBJaFBbCO7CJMdp5f+LQjUoqNEPOllm/maAR/wDHTuv0UNudVy+f+iKqXp1IMU6eCRzbXNSWYAwvYkyDLHpoId3YMMzp21cbrBWgWsoiz/0KKCAwfACPfnzvFf3CCf0+UxfhiLb/AOSUwUt8LzBTOTyUcqlR6d7b6Jb59spkKxCiruIOyQyQGiUll06UwhtcpVJCQ8mVvx28T7QVJLIioX6VflbYJP5UQ6SsfXKeZZ1giM62z/iaEK6VvNBLAP0IKiS/vH/aBWU68wEe+/D5UbsjJ2TsPI9WotRGYlQ4VC5eNiD0r5PYIJlofn8ehAa1vaRgCIrFRZMvSYAnYwiE6qJ9IXLJiynYZdzN4GJxwACpRD7zsceJy14qQak7s90qhKnIXuGn8pgeQwcerhX2idJc8p6Djk8pYaXmKV9pewe9othN1T+QphUpikKTg1JcCUIkwJkAS1CiDxdQdJ8mTkS+Y3PFrVLLZEpA7EFdrKimyo7M/n0wdmI60RMLuQGjgl3Z6c8PxGq51JL416fXi50r502+IEyKmcR50mG8MjySvHCA06p0mjq0LYztgHulbsa8aM+3+wOaJ23xzJF1t/TczVsjoZZ/r5T9NYxDI9ofZWFSF/as4TDyXGgeqtNljVS31TJtAzO6xh4gVZylH1CJAe1d9wC4lSFa0LHonr0NTdWwPrnTifF9O42s626WaERJUbx527x9SJNKnke69kuMFXByxY+U47naPAEeD1UDHm1k3mYe8D09K5ccv9HtMbDNcj3eTEI8lsHbG0K1opZ3x7hPP1NExvZ5X27XZcNrsvSpUutCpetSiLrWlaXsYanTd2Y77dr03Zcc0W/IwOoV1Ja+f5nlz4JOZLMKJC8oTXC31VU9loiGD5dDo7RjDkhbfojqDEuMwh/oE86kP25anmHzsIOSHPbGCM1eOysEySruA/Qkj9N8Rl8RlEcYL1mYcW2xZVpmV/J0ILJdVuGmOMExpHYkJBBq8lyTAGLsP2mIupYXhavRFjICoi2E1HwIWpCWyoHi70FShXYB/e8J61RuGPNRUzx5lEwoyHLcL96ZQKqgYckT3WChwzGztp9dBJYIFzk/U2N2bMUBEheaDBySqb8kq6jJ39II0/r5TB+GO4+P40B3L7JI28hfTKxcNhJIBUSJiF7c7WqaglkG5W6UfwwgI6ya9k7keBsGd91lgl7T+G0St8pF5M1AiBApAGLsB2syCf51gwcdI1KKiEcZz3/QP4gyREciQs4VJyVVE1jfnkJcCQz3EqsCRpT9qhBBydkQ83JRkXYcuXQC0Ky8EebTk8pALmCsyAMdaOPuiXFH+Xdr+lMQz5R5DypghvaKgcvzNkFjd+ezAdO9zi1QpDPtnBhsQy9sCjC1gB8znv1k+Bi1CaAkt5aAKvDBlu1cP0QwaAkFe2YzcACCvBmcxWgA+2GM84mHm4bxrVY6Lp9aZ6ePxno3vda3BOWTgaogK7zod/ZLdOiI2XO/h6AzIxXUb7LPKi1xwr7sDiKt8PCBBgWwAudzQ0DX6sIFus5hWavy62hBi/ZOrmgMvR3sXd4+5FOtIFjul0Tfe1bmQWy0ailVnPBLKswTVa9jCTJC6WWBYQDzn1/bK2PpnO0JZrGug5HwTvjyMtfwUKibLdoCsKZi2LHm6twewTCUNoAR4wlbodRXYQn/AGvT5SVmaADoyLzmfyUhHKhD66N6fuKpTgjT2ivmFhXoBCoA4iCMC3bfvKj/AH8owcdoPofxofe3Xu8Yyrt9uxbiM0HqEb418yYkRElNLd1kZdqCKqFWrB+6N98CCoAopHIkFUvU8efrGXM8nj/RFq00j+7ctK2QkFnBGEoQI0Oe2FiCHCCOpqDsufWlIvyt4Pg+mZY/wYN/lGEQrvEj9sIpUiLX5YFSPcnEJ4HKcBBT6zNc+ExnY9R+11fDyR9U7R72xer/ANIYT2AJZqY/8yHD5Y3uRHIId/8AOgkU/wBqsLhdrAPawam0DzAVgPnGQXHYLGwjMIWP8/uRO4JO6vL6I4d7Lq9vidoFbb1vUlT70K1vLGp+sYA/fUIUS3lftIYsqgcm+bBGTodcNKw1fz2lwUbnsTyGIBTW8vEUFR8tyalYqgQ7QdnTL1FcumFlQDoHVr8Yj0bZb0L0uC8u0UB7WeaI/QQOpcBZjkA0ZpljiaKR6saESv3FaQxxBAxxOblBg+2W8RQUz0gMXCLmi789QQiA2CnvTDyRHA3ESYXLEUw1OWi2cTcmrqkLPZDiyWIK+4PkmkMrkMrGlSwCO12GiRWoeaH7IwEchrEQCkpl5JobUblYq4E37qADuqIGUwWgIho9kJVBqu8paCtX7kcmfcb+8ERRe0/li6f0BxvabBCx9xuqCY/WxawcVKPg+JQJEvHckW2wo+4jvGMnjfB2JSW6zknUvbODyJTBciXUJ1owpHHUVudqLMM/QRmPNGNCUqeMJdj/AJLFU8YmH58rKneOs5pd39VC4JRWeeHssigawChfxKyYlE+BCCE7ouwitntOEOYX96L5HsPZAv5TVJkD0ZImuyJZO49kYJDavf4lmq4OJz7PiFFjtjAPXYQUAAoOwTHRp3Z0SMF8QTEePU4mSUgvl5mkcjTQQAeaqmyIVxgevCM8WvZxizdZ7ge6QNhqkpsY2oNaV5UBXohtGOREGlvuswmTo0//AGH+mEh9DcCrc8hbXFyGAbwZ06nHlECWZ8hbh7O0iO3S6ad4gHAYCJ7KyG9osZhnbFO7jfvGCgI3EquTAXA84MKjAVZAUMStNQc1vVwVx6UWxfFuxgkLKALWTKNdlZL1l7QFNQw54ZIH7wWNADlCKjDloaaDrPkBit9nmFGL8q0ZYhDDSwy3sY4u4rNd4AMWGl2lzRl7169w2ySLnUkWtZfWMISnmeyIe8w02oRSIiwInslfM9mgYp5mIJI/GD5T3RTQbFbA3ZlO8bVC4/6pDzZxzpmbH7TYxIYgGV7RGTAYIZgwQpxLWr3CHjQfeFb5+tY6AIzQr2luwMy3lKLpxcd1EPniSmXyJEjKWPnhSBS2W/tExb2ejz8yOwQsiORieihXJGT5SQmtdHhhgK8u3b8hYcEfHlfct5c5l9+J4gyAABQEvdW8S322gRj63kPkl8mEUkDbl4ieqMHjXz2rmbbR57tQfMzZ/XbGANmUnyRDwc7CQ5uQXbxQhbe8ueBKEUxIzuOCORL7ohowL2I9DKkWZllyqVoLdozCqbdm4GSgvs/DLUk5ltFwES9vj7Myw0PQFslawW7gvcfhVqR1NtdfjQ2OrDjUD3Ch6r3ctJFomrJZtxTcuDDNLykCbFOGtWGOsm4I1XAsWyci0YRgrKB3rrnKHa4/jXGkjIxFWs45BS4iADiEjRg9/wC7PZMygvfUJrIXFyuzlDUAAYCXdtUGo/vLYa/bYiIIUR6LjI0McOQFTkXOAkVjBktEThRkTsy/eub/AJKBF1FVN5gmUmCBA5UHDx7TKwK6tlHqLJc75RfH6yf9bD/0sP8A3k/7+f8AWT/tI/8ArIf+kn/SR/8AWT/rJ/3k/wCsh/7yf9JP+kh/6yf9JP8ArJ/0k/6SK/7sP/Szz/rI1AglK7h3VoS4wGfMeH8qcuPGmjz2Pkle6dzE37I3+6Ii18l/YI/Y+nbGxE7DfJeEfggmAE+AqUAz7cRtqgr/ABAEAigP0KnGtb8CBhjob3n7Q/o+tR6JwiII8k7Bs5vXBPnwLXu7OUa9hl/FYAba0Nb0rRZf539XecdPpAgDIMs79rR6JaCrKvAAkJHB8sYMbL7i83YwbUaQ3GiKsViE58QT8KsBwVEt6/pa2EFVNUw/fiUEGCB+We29mwMIXVysYO+GaihMdWOYgWE0L3I/M6H/AFAmdeVXxQm52d0v55kb4gTOQuDmuRqYGl9SpjpLB21qErqnRqXpUSImGGkwKABXxrelxA2TmqTR+VTjQdl640vo46QaKLQxFCBMvqABESLoCnJKmEMjWiWaBZUCEWI8jcxrcYAtQIJgX4llWwQscSune25ZoEqISmUvv7m0+5GiuIrq9coF/owoyyYhBCLK5LfdYMxNbSBxEJT2jfPZuVR0soZyFWFSVjUs0AOVg4Ef8giom4K/+EDOdyfgjxLGGvt8svWulboIZQ9VJ3Y3aU9TSodElzPFQ8YwnOY2t0dTRZsNL4qhFlckg+44FhXHBvVzGpsVozfXnqgrYCIX22OUUzwpbi/YKV5L3YnB7Ih1WKu2RSAIQiVhtus1KcUpy+VSsB2v+EJMSxE4wasUynr/ABxG7CDhSEO3AUpRI9DGl6J0S+uR6C/lPUrZbB2m2pUwhW+NbzhhqBX9tIOpABJtSKyuOJT75krPQL3sKIhrRft5MU5yVuVYpKx+5cTAXLAKCs4TqHaNwZf2M+REIUgMX3WV8Zi10KG3uDp4ypYI0qM0ohwXqlXhURW9utnkTMF4i8X9QHTftevvGonaDztDt5EXp2YKxreSZmD+IGmQ8krZTuwSfFV/XnheIF/UzHa+df8AHZ37+piKF/x2Y7sp/wAJlmhD3H/M3hs+zxqeDLkDhPAho/g1rYMv1xsj5iGb5eNq6pAIecr77KcGmX4JeWGoxTsxY4sHzfChp3t9z4IEbzS3y1L7TxlVl8AYvDW7jli0rb1BgqrtxLbc6IE1MYpfMqQzR+dU9JANB23GrqK+WhKaAl30z/4B0CJpWw0WXrjqVq61uqussbSLpc0AUSG2z1le6llzvVjjEVJ3tyrgKo8Xi3EbWgSWQECy6Ca93BC8ZXLCxKNTdCAa3HEtfRL+JZAXqPrhXjZKzG4vCj3JQwF0Ku3OKlyjLpS9zCW83t3w7VqgWDjnKN1lLAQcLLEElCHQMFyx7gMp8lo9Qgw8jDMUl5Ah173tyiYjyA/OYpavto8zH/YdMND4gErKl7cTB0GVM7mLlO/kYSma7gm/eFltdaRqpW4TxpawbmXlsKWunFjz5vHEbSFw3efdhUorP3BioPv91WYTBboeeJA9nKxKJplX0z4d7ZqMmV3b8QCSqAcUxItaXmTAwu/3cYEqYl6jveiF9K9KemdDGxv8GjabcakxsuVoaZ2LoGhQ95TQw0LJVykuBJYS4q5VS4SvURKhMSkrU3417x6F61pey+sGl7yAVxSTQxV7xm/b7euFa2wgB3YADFsVEYrm7rRm1lMCSlIotnPBx54DAmJXPrwRwLcwmcpU/dLulzayYTcyboNAowMGA2MCNjIMWveR/wAW1NtrlQGVAsaiyiNFIK2ly5e7OmNWYg1tdtb6/EYStcR0ekaPWOqrLKTvGbfs+Z3VSjAJ/FQteLhfuHihSYGDFRY7ZopezKyukBsBW2/MROv9KOKIQu8pUbcwcwuIeg5ASxgi0Ixe8E5aYLHmNSRvM4SNO0MkizMZpWBEmq6+8H80WEjSRA7qNLSAWBYqKnhxEfAIwnr8RX2Q4vdV3g/6loMH6CB+PkDfAlLButU8LhuIbcpRasphfIfON2fwb/Gzvxre63QImty9Mfnuy/wLl63oGy+ihseivQzpUrYTjYcIrEJgwPImBhEVxIYyz+BNXBRWh8tCkmEx1qQXEeJCfRfZJpTqq6FlQjtT/K9ojUGHdmDBUQ0FRcovJPWcO1QYkg1KJsqeVp4quZN997mONAkEYq3PS1U4bxAlHE9MqWERaKoAYtUgCP17HNQKBpuZeREUnS+GVCxO+FURwspiBPjrXgThEKjQRUIC7nARH0iDtCO/aCrdnZ9706V69pUZexxo7b97eJehpWrpe2l1egaVvuXMbWtL3Yl650PiY052Vq7samtvRNGUbMm7G2ulcxre6kCpRMaVKQJQSiOgxtAmJjRUo0o6+IdCtL0x0C9h0TeSt5retSq2ZJzq6VsvR1JW24mytla4/MvpnVvQjKekSpbL0rZmZ6F7DfW36l7a2Y0dta11eOs9I230qrfnZfW+tWXL21rnoXtToX1Kevjr1K227MR6tu9NmNKjrWw6FbT8u919Qejidtr+XjR6F6H4eNb6htP/AJN6kc9Guk9M2Gw2kdM7q6zuPwU2HQztxsGW6/e939uibb3Z/Bvdex22dU6Vakrp51xsNDpY6x0sbfrYdEdL3joVriVrnpvSx0ca3obr6FbMS92NlbKJWqSzrG92G8YmlbHpVXXN7urZTKhq6nTPwK/L4/Hz1yXtrov4SaGuPyAnxK3O2ulnrX+aTO56WNeNn1+Ab6fwb1OrbvvYaXtrpX0TfUxLheov499FhL2YPwO34fH4dw1dMbKdDbjom4dmZe6uhjrGgP4VMNU2m82V1LNCMPwszEvoLey3pHSrZTpe29ufy7NKrqXrXTeiPTNfvZn8e+swnPSzDoBpW40rbUB0eh9dfGrq9a9fvZnfcvbfTx03XiM43A6/GlOy9xuwdBrb26Fw2Vq6Js4l63vvWsbDMIdK+gbL0I772BvzoZ33KrpG1387KZTLldCoOw6FaDou7OlaVswb7mXXMNmNM7zebc63K0XS47B0Do063oX+WnuG/ENeOrndey9h87Dca3sq9V3VKldc/wDm46B0c9DOyt2XoXr20s2XtrcbsdHHQenT1TYy+he86Nuhpet7WXrb+DXSNluzPVrQ34lu756V6Xst6J0M7c9Q31sdtu46mduOk7s/hv5J1cdG3YdW9SO3Gt9KtMw3mw3n/wAc2O6//g11a2PRMReu9I2j/wDBt6OfwbN5jQj+bfWOmveflXsHR1N17a6eNOPyHZl/BxuNSPWrpm02OyvwK21K28biLsvV/It2XDdnbX4w9CtpGDuxsTpX1L2mg/iY6v3pj8a5eqb8an596LobzU0dbrdfWvqP4Y9T62Vvz0Pvp3186VKdbejUzqaZNGXvHTOtbnU2mxhs+ujnrut9Z23sxpUdt760ehe2/wAPt1C/wa1xoPSOiaVp3l9c1Mac6XpjrdunUqVrjbcxsdlfjZ25NwbTYfhU7q2Yn3GupjffTzL31rXSrS4dezQ33vx0K6T+GMNOdt6Vq9B6Fy+sb76FbR6taVrjoX1L2Y2XMStlupetbnUd33K23sOgRISzU/MN+JW+3W+i6Y2PSDZWlfgYJcyb3THQJcp23sSurezGtbjdUvQeq7ca42/f5WOo7SYmN9zGlPQphK/DJX4DXQx1bibT8atb6oHWx1b/ABR6BvXfe69rvNl7XPXrp3Fd9u7P4VdSndjdjaba/ErZRszsemw1rR2ZdV0zsz0r/DrQJXTz1L3GmIb8bfrZUvcdN6d63pncdK47R1XW9Kg6nSxrcqV1jbetTGtbTe7jTHS4lzExsZjTOvH4nOla1pW42GmNt7M6p0E3c6H4xHr1pWy/xM7amNp0cau+tK61dfEvfUr8K9962y2t6XHZet9G9l6L1F/BuWw0vS9b1dTZcuXqS9ly9163Ldly9L0vYaWy9t1DZcuXMaXWl9C9t7Vl776BBrTiXvvQdF3f/9k="
                 alt="Partner Logos"
                 style="width:100%;max-width:420px;height:auto;
                        object-fit:contain;display:block;"/>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Stats Row
st.markdown("""
    <div class="stats-row">
        <div class="stat-card green">
            <p class="stat-number">8+</p>
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
    first_name = st.session_state.submitted_name.split()[0] if st.session_state.submitted_name else ""
    st.markdown(f"""
        <div class="success-wrapper">
            <div class="success-circle">✅</div>
            <div class="success-title">Registration Successful, {first_name}! 🎉</div>
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
                <div class="success-step">📱 Watch for our call</div>
                <div class="success-step">🚀 Get ready to learn!</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Toggle state init
    if "show_email" not in st.session_state:
        st.session_state.show_email = False

    # Verify your email — styled as card, same row feel
    st.markdown("""
        <style>
        div[data-testid="stColumns"] .stButton > button {
            background: #ffffff !important;
            color: #388e3c !important;
            border: 2px solid #c8e6c9 !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
            animation: none !important;
            width: 100% !important;
        }
        div[data-testid="stColumns"] .stButton > button:hover {
            border-color: #66bb6a !important;
            background: #f1f8e9 !important;
            transform: translateY(-2px) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col_v1, col_v2, col_v3 = st.columns([1, 1, 1])
    with col_v1:
        if st.button("✉️ Verify your email", key="verify_email_btn"):
            st.session_state.show_email = not st.session_state.show_email
            st.rerun()
        if st.session_state.show_email:
            st.markdown(f"""
                <div style="background:linear-gradient(135deg,#e8f5e9,#f1f8e9);
                    border:2px solid #66bb6a;border-radius:10px;padding:10px 16px;
                    text-align:center;font-size:0.85rem;font-weight:600;color:#1b5e20;margin-top:6px;">
                    📧 <span style="color:#e65100;">{st.session_state.submitted_email}</span>
                </div>
            """, unsafe_allow_html=True)

    # ── AI CHATBOT SECTION ────────────────────────────────────────────────────
    st.markdown(f"""
        <div class="chatbot-container">
            <div class="chatbot-header">
                <span style="font-size:2rem;">🤖</span>
                <div style="flex:1;">
                    <p class="chatbot-title">LearnMate AI Assistant</p>
                    <p class="chatbot-subtitle">Ask me anything about your course, fees, schedule, or career prospects!</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Show initial greeting if no chat yet
    if not st.session_state.chat_history:
        course = st.session_state.submitted_course
        name = st.session_state.submitted_name
        greeting = f"Hi {name}! 👋 Congratulations on registering for **{course}** at LearnMate! I'm your AI assistant. You can ask me anything — course syllabus, duration, career paths, or any other questions you have. How can I help you today?"
        st.session_state.chat_history.append({"role": "assistant", "content": greeting})

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Typing indicator — AI reply வரும்முன்னே காட்டு
    if st.session_state.get("typing"):
        st.markdown("""
            <div class="typing-indicator">
                🤖&nbsp;
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        """, unsafe_allow_html=True)

    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.chat_input("Ask your question here...")

    if user_input and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.typing = True
        st.rerun()

    if st.session_state.get("typing"):
        course = st.session_state.submitted_course
        name = st.session_state.submitted_name
        last_user_msg = next(
            (m["content"] for m in reversed(st.session_state.chat_history) if m["role"] == "user"), ""
        )
        ai_reply = get_smart_reply(last_user_msg, course, name)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.session_state.typing = False
        st.rerun()

    # Register Another button - right side
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn2:
        if st.button("📝 Register Another Form"):
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
            with st.spinner("✨ Submitting your form... please wait!"):
                result = submit_to_google_form(form_data)

            if result["success"]:
                log_successful_submission(form_data)
                st.session_state.submitted = True
                st.session_state.submitted_course = course
                st.session_state.submitted_name = name
                st.session_state.submitted_email = email
                st.rerun()
            else:
                st.error(f"⚠️ Submission failed: {result['message']}")
                st.info("💡 Please try again or contact us at skilzlearn.gpc@gmail.com")
