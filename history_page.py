"""
history_page.py - Display Chat History (ALL CONTENT VISIBLE)
All headings, content, icons, and buttons fully visible
"""

import streamlit as st
from database_manager import get_db
from datetime import datetime

def show_chat_history_page():
    """Render the chat history page - All content visible"""
    
    # Check if user is logged in
    if not st.session_state.get("submitted"):
        st.error("❌ Please complete registration first!")
        st.stop()
    
    user_email = st.session_state.submitted_email
    user_name = st.session_state.submitted_name
    course = st.session_state.submitted_course
    
    # CSS for maximum visibility
    st.markdown("""
    <style>
    /* Ensure all text is visible */
    body, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: inherit !important;
    }
    
    /* Headers styling */
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1b5e20 !important;
        margin: 20px 0 10px 0 !important;
        text-align: left;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #555 !important;
        margin: 10px 0 20px 0 !important;
        text-align: left;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1b5e20 !important;
        margin: 20px 0 15px 0 !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Stats boxes */
    .stats-box {
        background-color: #f0f7f0 !important;
        border: 2px solid #1b5e20 !important;
        border-radius: 12px;
        padding: 20px !important;
        margin: 10px 0 !important;
        text-align: center;
    }
    
    .stats-label {
        font-size: 0.9rem;
        color: #666 !important;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .stats-value {
        font-size: 2rem;
        color: #1b5e20 !important;
        font-weight: 800;
    }
    
    /* Conversation items */
    .conversation-item {
        background-color: #f5f5f5 !important;
        border: 1px solid #ddd !important;
        border-radius: 8px;
        padding: 15px !important;
        margin: 10px 0 !important;
        color: #333 !important;
    }
    
    .conversation-time {
        color: #666 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Content boxes */
    .question-box {
        background-color: #e8f5e9 !important;
        color: #1b1b1b !important;
        padding: 15px !important;
        border-radius: 8px;
        border-left: 5px solid #1b5e20 !important;
        margin: 12px 0 !important;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .answer-box {
        background-color: #fff3e0 !important;
        color: #1b1b1b !important;
        padding: 15px !important;
        border-radius: 8px;
        border-left: 5px solid #e65100 !important;
        margin: 12px 0 !important;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .course-badge {
        background-color: #fff3e0 !important;
        color: #e65100 !important;
        padding: 10px 15px !important;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
        font-size: 0.95rem;
    }
    
    /* Button styling */
    .stButton > button {
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        min-height: 48px !important;
        border-radius: 8px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0f7f0 !important;
        border-radius: 8px !important;
        border: 1px solid #c8e6c9 !important;
    }
    
    .streamlit-expanderHeader p {
        color: #1b5e20 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Dividers */
    hr {
        border-color: #ddd !important;
        margin: 20px 0 !important;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #e3f2fd !important;
        color: #1976d2 !important;
    }
    
    .stSuccess {
        background-color: #c8e6c9 !important;
        color: #1b5e20 !important;
    }
    
    .stWarning {
        background-color: #fff3e0 !important;
        color: #e65100 !important;
    }
    
    /* Ensure visibility of all content */
    .stMarkdown {
        color: inherit !important;
    }
    
    .stMetric {
        background-color: #f0f7f0 !important;
        border-radius: 8px;
        padding: 15px !important;
    }
    
    .stMetric label {
        color: #666 !important;
        font-weight: 600 !important;
    }
    
    .stMetric .metric-value {
        color: #1b5e20 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="header-title">💬 Your Chat History</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">View all your conversations with the AI Assistant</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get chat history
    db = get_db()
    chat_history = db.get_user_history(user_email)
    
    # Stats Section
    st.markdown('<div class="section-header">📊 Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-label">Total Messages</div>
            <div class="stats-value">{len(chat_history)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-label">Course</div>
            <div class="stats-value">{course}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-label">Student</div>
            <div class="stats-value">{user_name.split()[0]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Conversations Section
    st.markdown('<div class="section-header">📝 Conversations</div>', unsafe_allow_html=True)
    
    # Display messages
    if not chat_history:
        st.info("💭 No conversations yet. Start chatting with the AI to see your messages here!")
    else:
        for idx, msg in enumerate(chat_history):
            # Format timestamp
            try:
                time_obj = datetime.fromisoformat(msg['created_at'])
                time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
            except:
                time_str = msg['created_at']
            
            # Create expander for each message
            with st.expander(f"🕐 {time_str}", expanded=False):
                
                # Question Section
                st.markdown("**👤 Your Question:**")
                st.markdown(f'<div class="question-box">{msg["user_message"]}</div>', unsafe_allow_html=True)
                
                st.markdown("")  # Spacing
                
                # Answer Section
                st.markdown("**🤖 AI Response:**")
                st.markdown(f'<div class="answer-box">{msg["ai_response"]}</div>', unsafe_allow_html=True)
                
                st.markdown("")  # Spacing
                
                # Course Info
                st.markdown(f'<div class="course-badge">📚 Course: {msg["course"]}</div>', unsafe_allow_html=True)
                
                st.markdown("")  # Spacing
                
                # Delete button
                col_del, col_space = st.columns([0.2, 0.8])
                with col_del:
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        db.delete_message(msg['id'])
                        st.success("✅ Message deleted!")
                        st.rerun()
        
        st.markdown("---")
        
        # Clear all section
        st.markdown("### 🧹 Clear History")
        col_clear, col_info = st.columns([0.3, 0.7])
        with col_clear:
            if st.button("🗑️ Clear All History", use_container_width=True):
                if st.session_state.get("confirm_clear"):
                    db.clear_user_history(user_email)
                    st.session_state.confirm_clear = False
                    st.success("✅ All history cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm")
    
    st.markdown("---")
    
    # Back button
    st.markdown("### 🔙 Navigation")
    if st.button("← Back to Chat", use_container_width=True, type="primary"):
        st.session_state.show_history_page = False
        st.rerun()
