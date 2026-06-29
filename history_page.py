"""
history_page.py - Professional Chat History with Admin PDF Download
Regular users: View only their chat history
Admins: View all users' chats + Download as PDF
"""

import streamlit as st
from database_manager import get_db
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def generate_pdf_for_user(user_email, user_name, course, user_chats):
    """Generate PDF for a single user's chat history"""
    
    # Create PDF in memory
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1b5e20'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1b5e20'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    user_info_style = ParagraphStyle(
        'UserInfo',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
    )
    
    question_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1b5e20'),
        spaceAfter=8,
        leftIndent=12,
        fontName='Helvetica-Bold'
    )
    
    answer_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#e65100'),
        spaceAfter=8,
        leftIndent=12,
        fontName='Helvetica-Bold'
    )
    
    message_style = ParagraphStyle(
        'Message',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        leftIndent=24,
        alignment=TA_JUSTIFY
    )
    
    # Build PDF content
    content = []
    
    # Title
    content.append(Paragraph("LearnMate - Chat History Report", title_style))
    content.append(Spacer(1, 0.3*inch))
    
    # User Information Section
    content.append(Paragraph("User Information", heading_style))
    user_info_data = [
        ['Name:', user_name],
        ['Email:', user_email],
        ['Course:', course],
        ['Total Messages:', str(len(user_chats))],
        ['Generated:', datetime.now().strftime("%d %b, %Y • %I:%M %p")]
    ]
    
    user_info_table = Table(user_info_data, colWidths=[1.5*inch, 4*inch])
    user_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1b5e20')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#a5d6a7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    content.append(user_info_table)
    content.append(Spacer(1, 0.3*inch))
    
    # Conversations Section
    if user_chats:
        content.append(Paragraph("Chat Conversations", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        for idx, chat in enumerate(user_chats, 1):
            try:
                time_obj = datetime.fromisoformat(chat['created_at'])
                time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
            except:
                time_str = chat['created_at']
            
            # Conversation number and timestamp
            content.append(Paragraph(f"<b>Message #{idx}</b> - {time_str}", user_info_style))
            
            # Question
            content.append(Paragraph("👤 Question:", question_style))
            question_text = chat['user_message'].replace('<', '&lt;').replace('>', '&gt;')
            content.append(Paragraph(question_text, message_style))
            
            # Answer
            content.append(Paragraph("🤖 Response:", answer_style))
            answer_text = chat['ai_response'].replace('<', '&lt;').replace('>', '&gt;')
            content.append(Paragraph(answer_text, message_style))
            
            # Course
            content.append(Paragraph(f"<b>Course:</b> {chat['course']}", user_info_style))
            content.append(Spacer(1, 0.2*inch))
            
            # Page break after every 5 messages
            if idx % 5 == 0 and idx < len(user_chats):
                content.append(PageBreak())
    else:
        content.append(Paragraph("No conversations yet", heading_style))
    
    # Build PDF
    doc.build(content)
    pdf_buffer.seek(0)
    return pdf_buffer

def generate_pdf_all_users(all_users, db):
    """Generate PDF for all users' chat history"""
    
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1b5e20'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1b5e20'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    message_style = ParagraphStyle(
        'Message',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        leftIndent=24,
        alignment=TA_JUSTIFY
    )
    
    content = []
    
    # Title
    content.append(Paragraph("LearnMate - All Users Chat History Report", title_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Summary
    total_chats = db.get_total_chats()
    total_users = db.get_total_users()
    
    summary_data = [
        ['Total Users:', str(total_users)],
        ['Total Messages:', str(total_chats)],
        ['Report Generated:', datetime.now().strftime("%d %b, %Y • %I:%M %p")]
    ]
    
    summary_table = Table(summary_data, colWidths=[1.5*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1b5e20')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#a5d6a7')),
    ]))
    
    content.append(summary_table)
    content.append(Spacer(1, 0.3*inch))
    
    # All Users' Chats
    for user_idx, user in enumerate(all_users):
        user_email = user['user_email']
        user_name = user['user_name']
        course = user['course']
        
        content.append(Paragraph(f"User #{user_idx + 1}: {user_name}", heading_style))
        
        user_info = f"<b>Email:</b> {user_email} | <b>Course:</b> {course} | <b>Messages:</b> {user['total_messages']}"
        content.append(Paragraph(user_info, ParagraphStyle(
            'UserSummary',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            spaceAfter=10,
        )))
        
        user_chats = db.get_user_chat_history(user_email)
        
        if user_chats:
            for chat_idx, chat in enumerate(user_chats, 1):
                try:
                    time_obj = datetime.fromisoformat(chat['created_at'])
                    time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
                except:
                    time_str = chat['created_at']
                
                content.append(Paragraph(f"<b>Q:</b> {chat['user_message'][:100]}... [{time_str}]", message_style))
                content.append(Spacer(1, 0.05*inch))
        
        content.append(Spacer(1, 0.2*inch))
        
        if user_idx < len(all_users) - 1:
            content.append(PageBreak())
    
    doc.build(content)
    pdf_buffer.seek(0)
    return pdf_buffer

def show_chat_history_page():
    """Render the chat history page - Professional UI with PDF Download"""
    
    if not st.session_state.get("submitted"):
        st.error("❌ Please complete registration first!")
        st.stop()
    
    # Professional CSS Styling
    st.markdown("""
    <style>
    /* Header Section */
    .header-section {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #e65100 100%);
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(27, 94, 32, 0.15);
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-subtitle {
        font-size: 1rem;
        margin-top: 8px;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Admin Badge */
    .admin-badge-container {
        background-color: #fff3e0;
        border: 2px solid #e65100;
        border-radius: 12px;
        padding: 12px 20px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(230, 81, 0, 0.1);
    }
    
    .admin-badge-text {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e65100;
    }
    
    /* Statistics Cards */
    .stat-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border: 2px solid #a5d6a7;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.08);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(27, 94, 32, 0.15);
    }
    
    .stat-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #558b2f;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1b5e20;
        margin: 0;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1b5e20;
        margin: 30px 0 20px 0;
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 12px;
        border-bottom: 3px solid #1b5e20;
    }
    
    /* Tab Buttons */
    .tab-buttons {
        display: flex;
        gap: 10px;
        margin: 20px 0;
    }
    
    /* Conversation Cards */
    .conversation-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 0;
        margin: 15px 0;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .conversation-card:hover {
        box-shadow: 0 8px 24px rgba(27, 94, 32, 0.1);
        border-color: #66bb6a;
    }
    
    .conversation-header {
        background: linear-gradient(90deg, #f0f7f0 0%, #f1f8e9 100%);
        padding: 16px 20px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .conversation-time {
        font-size: 0.9rem;
        font-weight: 600;
        color: #1b5e20;
    }
    
    .question-section {
        padding: 20px;
        background-color: #e8f5e9;
        border-left: 5px solid #1b5e20;
    }
    
    .answer-section {
        padding: 20px;
        background-color: #fff3e0;
        border-left: 5px solid #e65100;
    }
    
    .message-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    
    .message-content {
        font-size: 0.95rem;
        color: #1a1a1a;
        line-height: 1.6;
    }
    
    .course-badge {
        background-color: #fff3e0;
        color: #e65100;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 15px;
    }
    
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #f1f8e9 0%, #fff9c4 100%);
        border: 2px dashed #a5d6a7;
        border-radius: 12px;
        margin: 30px 0;
    }
    
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    db = get_db()
    user_email = st.session_state.submitted_email
    user_name = st.session_state.submitted_name
    course = st.session_state.submitted_course
    
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "show_admin_login" not in st.session_state:
        st.session_state.show_admin_login = False
    if "admin_email_entered" not in st.session_state:
        st.session_state.admin_email_entered = ""
    if "admin_view_type" not in st.session_state:
        st.session_state.admin_view_type = "own"
    
    # ADMIN VIEW
    if st.session_state.is_admin:
        admin_name = db.get_admin_name(st.session_state.admin_email_entered)
        
        st.markdown(f"""
        <div class="header-section">
            <div class="header-title">💬 Chat History Dashboard</div>
            <div class="header-subtitle">Administrator View - Monitor and manage all conversations</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_badge, col_logout = st.columns([0.7, 0.3])
        with col_badge:
            st.markdown(f"""
            <div class="admin-badge-container">
                <div class="admin-badge-text">👑 Admin: {admin_name}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_logout:
            if st.button("🔒 Logout", use_container_width=True):
                st.session_state.is_admin = False
                st.session_state.admin_email_entered = ""
                st.rerun()
        
        st.markdown("---")
        
        # Tab Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Your Chat History", use_container_width=True, key="tab_own"):
                st.session_state.admin_view_type = "own"
                st.rerun()
        
        with col2:
            if st.button("👥 Users' Chat History", use_container_width=True, key="tab_users"):
                st.session_state.admin_view_type = "all_users"
                st.rerun()
        
        st.markdown("---")
        
        # OWN CHAT HISTORY
        if st.session_state.admin_view_type == "own":
            st.markdown('<div class="section-header">📋 Your Personal Chat History</div>', unsafe_allow_html=True)
            
            user_chats = db.get_user_chat_history(user_email)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Your Messages</div>
                    <div class="stat-value">{len(user_chats)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Course</div>
                    <div class="stat-value">{course.split()[0]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Student Name</div>
                    <div class="stat-value">{user_name.split()[0]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            if user_chats:
                # Download PDF Button
                col_pdf, col_space = st.columns([0.3, 0.7])
                with col_pdf:
                    pdf_buffer = generate_pdf_for_user(user_email, user_name, course, user_chats)
                    st.download_button(
                        label="📥 Download as PDF",
                        data=pdf_buffer,
                        file_name=f"{user_name}_chat_history.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                st.markdown('<div class="section-header">📝 Your Conversations</div>', unsafe_allow_html=True)
                
                for idx, msg in enumerate(user_chats):
                    try:
                        time_obj = datetime.fromisoformat(msg['created_at'])
                        time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
                    except:
                        time_str = msg['created_at']
                    
                    st.markdown(f"""
                    <div class="conversation-card">
                        <div class="conversation-header">
                            <div class="conversation-time">🕐 {time_str}</div>
                        </div>
                        <div class="question-section">
                            <div class="message-label">👤 Your Question</div>
                            <div class="message-content">{msg['user_message']}</div>
                        </div>
                        <div class="answer-section">
                            <div class="message-label">🤖 AI Response</div>
                            <div class="message-content">{msg['ai_response']}</div>
                        </div>
                        <div style="padding: 15px 20px;">
                            <div class="course-badge">📚 {msg['course']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-icon">💭</div>
                    <h3>No conversations yet</h3>
                </div>
                """, unsafe_allow_html=True)
        
        # ALL USERS CHAT HISTORY
        else:
            st.markdown('<div class="section-header">👥 All Users Chat History</div>', unsafe_allow_html=True)
            
            all_users = db.get_all_users()
            total_chats = db.get_total_chats()
            total_users = db.get_total_users()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total Users</div>
                    <div class="stat-value">{total_users}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total Messages</div>
                    <div class="stat-value">{total_chats}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg = round(total_chats / total_users, 1) if total_users > 0 else 0
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Avg per User</div>
                    <div class="stat-value">{avg}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Download All Users PDF
            col_pdf_all, col_space = st.columns([0.3, 0.7])
            with col_pdf_all:
                if all_users:
                    pdf_all_buffer = generate_pdf_all_users(all_users, db)
                    st.download_button(
                        label="📥 Download All Users PDF",
                        data=pdf_all_buffer,
                        file_name=f"LearnMate_All_Users_Chat_History_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            
            search_email = st.text_input("🔍 Search user by email:", placeholder="Enter email to filter...")
            
            st.markdown("---")
            
            if not all_users:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <h3>No users yet</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="section-header">📝 Users & Conversations</div>', unsafe_allow_html=True)
                
                for user in all_users:
                    if search_email and search_email.lower() not in user['user_email'].lower():
                        continue
                    
                    with st.expander(f"📧 {user['user_email']} • {user['user_name']} • {user['total_messages']} messages"):
                        
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.markdown(f"**👤 Name:** {user['user_name']}")
                            st.markdown(f"**📧 Email:** {user['user_email']}")
                        with col_info2:
                            st.markdown(f"**📚 Course:** {user['course']}")
                            st.markdown(f"**💬 Messages:** {user['total_messages']}")
                        
                        user_chats = db.get_user_chat_history(user['user_email'])
                        
                        # Download Individual User PDF
                        if user_chats:
                            col_pdf_user, col_space = st.columns([0.3, 0.7])
                            with col_pdf_user:
                                pdf_user_buffer = generate_pdf_for_user(user['user_email'], user['user_name'], user['course'], user_chats)
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=pdf_user_buffer,
                                    file_name=f"{user['user_name']}_chat_history.pdf",
                                    mime="application/pdf",
                                    key=f"pdf_{user['user_email']}"
                                )
                        
                        st.markdown("---")
                        
                        if user_chats:
                            for chat in user_chats:
                                try:
                                    time_obj = datetime.fromisoformat(chat['created_at'])
                                    time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
                                except:
                                    time_str = chat['created_at']
                                
                                st.markdown(f"""
                                <div class="conversation-card">
                                    <div class="conversation-header">
                                        <div class="conversation-time">🕐 {time_str}</div>
                                    </div>
                                    <div class="question-section">
                                        <div class="message-label">👤 Question</div>
                                        <div class="message-content">{chat['user_message']}</div>
                                    </div>
                                    <div class="answer-section">
                                        <div class="message-label">🤖 Response</div>
                                        <div class="message-content">{chat['ai_response']}</div>
                                    </div>
                                    <div style="padding: 15px 20px;">
                                        <div class="course-badge">📚 {chat['course']}</div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Delete button
                        if st.button("🗑️ Delete All", key=f"admin_del_{user['user_email']}", use_container_width=True):
                            db.clear_user_history(user['user_email'])
                            st.success(f"✅ Deleted all chats for {user['user_name']}")
                            st.rerun()
    
    # REGULAR USER VIEW
    else:
        st.markdown(f"""
        <div class="header-section">
            <div class="header-title">💬 Your Chat History</div>
            <div class="header-subtitle">Review your conversations with the AI Assistant</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        user_chats = db.get_user_chat_history(user_email)
        
        st.markdown('<div class="section-header">📊 Your Statistics</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Your Messages</div>
                <div class="stat-value">{len(user_chats)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Course</div>
                <div class="stat-value">{course.split()[0]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Student Name</div>
                <div class="stat-value">{user_name.split()[0]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if user_chats:
            st.info("ℹ️ **PDF Download:** Only administrators can download chat history as PDF. Please contact admin for assistance.")
            st.markdown('<div class="section-header">📝 Your Conversations</div>', unsafe_allow_html=True)
            
            for idx, msg in enumerate(user_chats):
                try:
                    time_obj = datetime.fromisoformat(msg['created_at'])
                    time_str = time_obj.strftime("%d %b, %Y • %I:%M %p")
                except:
                    time_str = msg['created_at']
                
                st.markdown(f"""
                <div class="conversation-card">
                    <div class="conversation-header">
                        <div class="conversation-time">🕐 {time_str}</div>
                    </div>
                    <div class="question-section">
                        <div class="message-label">👤 Your Question</div>
                        <div class="message-content">{msg['user_message']}</div>
                    </div>
                    <div class="answer-section">
                        <div class="message-label">🤖 AI Response</div>
                        <div class="message-content">{msg['ai_response']}</div>
                    </div>
                    <div style="padding: 15px 20px;">
                        <div class="course-badge">📚 {msg['course']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                    db.delete_message(msg['id'])
                    st.success("✅ Message deleted!")
                    st.rerun()
            
            st.markdown("---")
            
            col_clear, col_space = st.columns([0.3, 0.7])
            with col_clear:
                if st.button("🗑️ Clear All", use_container_width=True):
                    if st.session_state.get("confirm_clear"):
                        db.clear_user_history(user_email)
                        st.session_state.confirm_clear = False
                        st.success("✅ All history cleared!")
                        st.rerun()
                    else:
                        st.session_state.confirm_clear = True
                        st.warning("⚠️ Click again to confirm")
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">💭</div>
                <h3>No conversations yet</h3>
                <p>Start chatting with the AI to see your messages here</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Secret Admin Button
        col_secret, col_space = st.columns([0.05, 0.95])
        with col_secret:
            if st.button("⚙️", help="Settings"):
                st.session_state.show_admin_login = not st.session_state.show_admin_login
        
        if st.session_state.show_admin_login:
            st.markdown("### 🔐 Admin Login")
            st.warning("⚠️ Authorized personnel only")
            
            admin_id = st.text_input("Admin ID", key="admin_id_input")
            admin_password = st.text_input("Admin Password", type="password", key="admin_pwd_input")
            
            col_login, col_cancel = st.columns(2)
            with col_login:
                if st.button("🔓 Login", use_container_width=True):
                    if admin_id and admin_password:
                        if db.verify_admin(admin_id, admin_password):
                            st.session_state.is_admin = True
                            st.session_state.admin_email_entered = admin_id
                            st.success(f"✅ Welcome Admin!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
                    else:
                        st.warning("⚠️ Please enter both fields")
            
            with col_cancel:
                if st.button("✕ Cancel", use_container_width=True):
                    st.session_state.show_admin_login = False
                    st.rerun()
    
    st.markdown("---")
    
    if st.button("← Back to Chat", use_container_width=True, type="primary"):
        st.session_state.show_history_page = False
        st.rerun()
