"""
history_page.py - Display Chat History (COMPLETELY FIXED)
Shows clean question & answer format - No HTML code!
"""

import streamlit as st
from database_manager import get_db
from datetime import datetime

def show_chat_history_page():
    """Render the chat history page"""
    
    # Check if user is logged in
    if not st.session_state.get("submitted"):
        st.error("❌ Please complete registration first!")
        st.stop()
    
    user_email = st.session_state.submitted_email
    user_name = st.session_state.submitted_name
    course = st.session_state.submitted_course
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 40%, #e65100 100%);
        border-radius: 20px; padding: 30px 40px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(27,94,32,0.25);">
        <h1 style="color: white; margin: 0; font-size: 2rem;">💬 Your Chat History</h1>
        <p style="color: rgba(255,255,255,0.85); margin: 8px 0 0 0;">View all your conversations with the AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get chat history
    db = get_db()
    chat_history = db.get_user_history(user_email)
    
    # Stats Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Messages", value=len(chat_history))
    
    with col2:
        st.metric(label="Course", value=course)
    
    with col3:
        st.metric(label="Student", value=user_name.split()[0])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display messages
    if not chat_history:
        st.info("💭 No conversations yet. Start chatting with the AI to see your messages here!")
    else:
        st.markdown("### 📝 Conversations")
        
        for idx, msg in enumerate(chat_history):
            # Format timestamp
            try:
                time_obj = datetime.fromisoformat(msg['created_at'])
                time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
            except:
                time_str = msg['created_at']
            
            # Message Container
            with st.container():
                col_msg, col_del = st.columns([0.95, 0.05])
                
                with col_msg:
                    # Timestamp
                    st.caption(f"🕐 {time_str}")
                    
                    # Question
                    st.markdown("**👤 Your Question:**")
                    st.write(msg['user_message'])
                    
                    # Answer
                    st.markdown("**🤖 AI Response:**")
                    st.write(msg['ai_response'])
                    
                    # Course Info
                    st.markdown(f"📚 **Course:** {msg['course']}")
                    
                    st.divider()
                
                with col_del:
                    if st.button("🗑️", key=f"del_{idx}", help="Delete"):
                        db.delete_message(msg['id'])
                        st.success("✅ Deleted!")
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Clear all button
        if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
            if st.session_state.get("confirm_clear"):
                db.clear_user_history(user_email)
                st.session_state.confirm_clear = False
                st.success("✅ All history cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm deletion")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Chat", use_container_width=True, type="primary"):
        st.session_state.show_history_page = False
        st.rerun()
