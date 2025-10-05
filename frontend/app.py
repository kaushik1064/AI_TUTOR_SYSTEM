# Main Streamlit app
"""
Main Streamlit application for AI Tutor System
Entry point for the web interface
"""

import streamlit as st
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components.chat_interface import render_chat_interface, render_quick_actions, render_emotion_tracker
from frontend.components.dashboard import render_dashboard
from frontend.components.reports import render_reports_page

# Configure Streamlit page
st.set_page_config(
    page_title="AI Tutor - Your Learning Companion 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/ai-tutor-system',
        'Report a bug': 'https://github.com/your-repo/ai-tutor-system/issues',
        'About': """
        # AI Tutor System 🎓
        
        Your personal AI learning companion that provides:
        - Conversational tutoring and support
        - Academic progress tracking
        - Emotional wellbeing monitoring
        - Personalized study recommendations
        
        Built with ❤️ using Streamlit, FastAPI, and Google Gemini Pro
        """
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    
    .user-message {
        background: #e3f2fd;
        margin-left: 20px;
    }
    
    .assistant-message {
        background: #f3e5f5;
        margin-right: 20px;
    }
    
    .quick-action-btn {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin: 0.25rem;
    }
    
    .achievement-badge {
        background: #4caf50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
    
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #5a6fd8, #6a4190);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "Student"
    if 'user_token' not in st.session_state:
        st.session_state.user_token = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "💬 Chat"
    if 'user_subjects' not in st.session_state:
        st.session_state.user_subjects = []
    if 'academic_level' not in st.session_state:
        st.session_state.academic_level = "undergraduate"

def render_login_page():
    """Render login/registration page"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🎓 AI Tutor - Your Learning Companion")
    st.markdown("### Welcome! Let's help you achieve your academic goals ✨")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create two columns for login and registration
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔐 Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")
            submit_login = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit_login:
                if email and password:
                    # For demo purposes, accept any email/password
                    st.session_state.authenticated = True
                    st.session_state.user_name = email.split('@')[0].title()
                    st.session_state.user_token = "demo_token_12345"
                    st.success(f"Welcome back, {st.session_state.user_name}! 🎉")
                    st.rerun()
                else:
                    st.error("Please enter both email and password")
    
    with col2:
        st.subheader("📝 Create New Account")
        with st.form("register_form"):
            name = st.text_input("👤 Full Name")
            email_reg = st.text_input("📧 Email Address", key="reg_email")
            password_reg = st.text_input("🔒 Password", type="password", key="reg_password")
            
            academic_level = st.selectbox(
                "🎓 Academic Level",
                ["Elementary School", "Middle School", "High School", "Undergraduate", "Graduate"],
                help="Select your current academic level"
            )
            
            subjects = st.multiselect(
                "📚 Subjects of Interest",
                ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science", 
                 "English Literature", "History", "Geography", "Psychology", "Economics",
                 "Art", "Music", "Languages", "Philosophy", "Engineering"],
                help="Select subjects you're studying or interested in"
            )
            
            study_style = st.selectbox(
                "🎯 Preferred Learning Style",
                ["Visual (charts, diagrams)", "Auditory (discussions, explanations)", 
                 "Kinesthetic (hands-on practice)", "Mixed approach"],
                help="How do you learn best?"
            )
            
            submit_register = st.form_submit_button("Create Account", type="primary", use_container_width=True)
            
            if submit_register:
                if name and email_reg and password_reg:
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.session_state.user_token = "demo_token_12345"
                    st.session_state.user_subjects = subjects
                    st.session_state.academic_level = academic_level.lower().replace(' ', '_')
                    st.success(f"Account created successfully! Welcome, {name}! 🎉")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")
    
    # Demo features section
    st.markdown("---")
    st.subheader("✨ What you'll get with AI Tutor")
    
    feature_cols = st.columns(4)
    
    with feature_cols[0]:
        st.markdown("""
        **🤖 Smart Conversations**
        - Personalized tutoring
        - Emotional support
        - Study guidance
        - 24/7 availability
        """)
    
    with feature_cols[1]:
        st.markdown("""
        **📊 Progress Tracking**
        - Understanding levels
        - Study time analytics
        - Subject performance
        - Learning trends
        """)
    
    with feature_cols[2]:
        st.markdown("""
        **📅 Smart Reminders**
        - Exam notifications
        - Study schedules
        - Deadline tracking
        - Priority management
        """)
    
    with feature_cols[3]:
        st.markdown("""
        **🎯 Personalized Insights**
        - AI recommendations
        - Learning patterns
        - Goal achievement
        - Performance analytics
        """)
    
    # Demo login option
    st.markdown("---")
    st.info("💡 **Quick Demo**: Use any email and password to try the system!")

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "🧭 Navigate to:",
            ["💬 Chat", "📊 Dashboard", "📅 Reminders", "📈 Reports", "⚙️ Settings"],
            key="nav_selector"
        )
        
        st.session_state.current_page = page
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Study Streak", "7 days", "2")
        with col2:
            st.metric("This Week", "12h", "3h")
        
        # Progress indicator
        st.markdown("### 🎯 Weekly Goal")
        progress = 75
        st.progress(progress / 100)
        st.caption(f"{progress}% complete")
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("📚 Start Study Session", use_container_width=True):
            st.session_state.current_page = "💬 Chat"
            st.rerun()
        
        if st.button("📊 View Progress", use_container_width=True):
            st.session_state.current_page = "📊 Dashboard"
            st.rerun()
        
        if st.button("📅 Check Reminders", use_container_width=True):
            st.session_state.current_page = "📅 Reminders"
            st.rerun()
        
        # Settings and logout
        st.markdown("---")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("Data refreshed!")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_token = None
            st.session_state.user_name = "Student"
            st.cache_data.clear()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("AI Assistant v1.0")
        st.caption("Built with Streamlit & Gemini Pro")

def render_reminders_page():
    """Render the reminders and calendar page"""
    st.title("📅 Exam Reminders & Study Calendar")
    
    # Add new reminder section
    with st.expander("➕ Add New Reminder", expanded=False):
        with st.form("add_reminder_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("📝 Title", placeholder="e.g., Math Final Exam")
                subject = st.text_input("📚 Subject", placeholder="e.g., Mathematics")
                exam_date = st.date_input("📅 Date")
            
            with col2:
                priority = st.selectbox("⚡ Priority", ["High", "Medium", "Low"])
                reminder_days = st.multiselect(
                    "🔔 Remind me", 
                    ["7 days before", "3 days before", "1 day before", "Day of exam"],
                    default=["3 days before", "1 day before"]
                )
                description = st.text_area("📄 Description (optional)", placeholder="Additional notes...")
            
            if st.form_submit_button("Add Reminder", type="primary"):
                st.success(f"✅ Reminder added: {title}")
                st.balloons()
    
    # Upcoming reminders
    st.subheader("🔔 Upcoming Reminders")
    
    # Mock reminder data
    import pandas as pd
    from datetime import datetime, timedelta
    
    reminders_data = [
        {
            'Title': 'Mathematics Final Exam',
            'Subject': 'Mathematics', 
            'Date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'Priority': '🔴 High',
            'Days Left': 15,
            'Status': 'Active'
        },
        {
            'Title': 'Physics Lab Report',
            'Subject': 'Physics',
            'Date': (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d'),
            'Priority': '🟡 Medium', 
            'Days Left': 8,
            'Status': 'Active'
        },
        {
            'Title': 'Chemistry Quiz',
            'Subject': 'Chemistry',
            'Date': (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d'),
            'Priority': '🔴 High',
            'Days Left': 12,
            'Status': 'Active'
        },
        {
            'Title': 'Literature Essay',
            'Subject': 'English',
            'Date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
            'Priority': '🟡 Medium',
            'Days Left': 20,
            'Status': 'Active'
        }
    ]
    
    df = pd.DataFrame(reminders_data)
    
    # Display reminders as cards
    for _, reminder in df.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{reminder['Title']}**")
                st.caption(f"Subject: {reminder['Subject']}")
            
            with col2:
                st.markdown(f"📅 {reminder['Date']}")
            
            with col3:
                if reminder['Days Left'] <= 3:
                    st.error(f"⚠️ {reminder['Days Left']} days")
                elif reminder['Days Left'] <= 7:
                    st.warning(f"⏰ {reminder['Days Left']} days")
                else:
                    st.info(f"📅 {reminder['Days Left']} days")
            
            with col4:
                st.markdown(reminder['Priority'])
            
            st.markdown("---")
    
    # Calendar view
    st.subheader("📅 Calendar View")
    
    # Simple calendar display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**This Week**\n📚 Study sessions: 5\n📝 Assignments due: 2")
    
    with col2:
        st.warning("**Next Week**\n🔬 Lab report due\n📊 Project presentation")
    
    with col3:
        st.error("**Upcoming**\n📋 Final exams\n🎯 Major deadlines")

def render_settings_page():
    """Render the settings and preferences page"""
    st.title("⚙️ Settings & Preferences")
    
    # User profile settings
    st.subheader("👤 Profile Settings")
    
    with st.form("profile_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=st.session_state.user_name)
            email = st.text_input("Email", value="student@example.com")
            academic_level = st.selectbox(
                "Academic Level",
                ["Elementary", "Middle School", "High School", "Undergraduate", "Graduate"],
                index=2
            )
        
        with col2:
            subjects = st.multiselect(
                "Subjects",
                ["Mathematics", "Physics", "Chemistry", "Biology", "Literature"],
                default=st.session_state.get('user_subjects', ["Mathematics", "Physics"])
            )
            study_style = st.selectbox(
                "Learning Style",
                ["Visual", "Auditory", "Kinesthetic", "Mixed"],
                index=3
            )
            timezone = st.selectbox(
                "Timezone",
                ["UTC", "EST", "PST", "IST"],
                index=3
            )
        
        if st.form_submit_button("Save Profile", type="primary"):
            st.session_state.user_name = name
            st.session_state.user_subjects = subjects
            st.success("Profile updated successfully!")
    
    # Notification settings
    st.subheader("🔔 Notification Preferences")
    
    enable_notifications = st.checkbox("Enable notifications", value=True)
    
    if enable_notifications:
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Study reminders", value=True)
            st.checkbox("Exam alerts", value=True)
            st.checkbox("Progress updates", value=True)
        
        with col2:
            st.checkbox("Motivational messages", value=True)
            st.checkbox("Weekly reports", value=True)
            st.checkbox("Achievement notifications", value=False)
    
    # AI tutor settings
    st.subheader("🤖 AI Tutor Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ai_personality = st.selectbox(
            "AI Personality",
            ["Friendly & Encouraging", "Professional & Direct", "Casual & Fun"],
            index=0
        )
        response_length = st.selectbox(
            "Response Length",
            ["Concise", "Detailed", "Adaptive"],
            index=2
        )
    
    with col2:
        use_emojis = st.checkbox("Use emojis in responses", value=True)
        proactive_suggestions = st.checkbox("Proactive study suggestions", value=True)
    
    # Study preferences
    st.subheader("📚 Study Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_session_length = st.slider("Default study session (minutes)", 15, 120, 45)
        break_reminder = st.checkbox("Break reminders", value=True)
    
    with col2:
        difficulty_level = st.selectbox("Preferred difficulty level", ["Beginner", "Intermediate", "Advanced"])
        auto_save = st.checkbox("Auto-save progress", value=True)
    
    # Data and privacy
    st.subheader("🔒 Data & Privacy") 
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export My Data", use_container_width=True):
            st.success("Data export initiated. You'll receive an email shortly.")
        
        if st.button("🗑️ Delete Account", use_container_width=True):
            st.error("Account deletion requires email confirmation.")
    
    with col2:
        data_retention = st.selectbox(
            "Data Retention",
            ["1 month", "6 months", "1 year", "Indefinite"],
            index=2
        )
        
        analytics_opt_in = st.checkbox("Help improve AI Tutor with usage analytics", value=True)
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            api_timeout = st.slider("API timeout (seconds)", 5, 30, 10)
            max_conversation_length = st.slider("Max conversation history", 10, 100, 50)
        
        with col2:
            enable_debug = st.checkbox("Enable debug mode", value=False)
            beta_features = st.checkbox("Enable beta features", value=False)

def main():
    """Main application function"""
    initialize_session_state()
    
    if not st.session_state.authenticated:
        render_login_page()
    else:
        # Render sidebar
        render_sidebar()
        
        # Render main content based on selected page
        if st.session_state.current_page == "💬 Chat":
            render_chat_interface()
            st.markdown("---")
            render_quick_actions()
            render_emotion_tracker()
            
        elif st.session_state.current_page == "📊 Dashboard":
            render_dashboard()
            
        elif st.session_state.current_page == "📅 Reminders":
            render_reminders_page()
            
        elif st.session_state.current_page == "📈 Reports":
            render_reports_page()
            
        elif st.session_state.current_page == "⚙️ Settings":
            render_settings_page()

if __name__ == "__main__":
    main()
