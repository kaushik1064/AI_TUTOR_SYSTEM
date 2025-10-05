# Chat UI component
"""
Chat interface component for Streamlit frontend
Handles the main conversation UI and interactions
"""

import streamlit as st
import requests
from datetime import datetime
from typing import List, Dict, Any

def render_chat_interface():
    """Render the main chat interface"""
    st.title("💬 Chat with Your AI Tutor")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = None
    
    # Session type selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        session_type = st.selectbox(
            "Session Type:",
            ["general", "study_session", "check_in", "exam_prep"],
            format_func=lambda x: {
                "general": "💬 General Chat",
                "study_session": "📚 Study Session", 
                "check_in": "🤗 Daily Check-in",
                "exam_prep": "🎯 Exam Preparation"
            }[x],
            key="session_type"
        )
    
    with col2:
        if st.button("🔄 New Session"):
            st.session_state.messages = []
            st.session_state.current_session_id = None
            st.rerun()
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # Show additional info for assistant messages
                if message["role"] == "assistant":
                    if message.get("emotion"):
                        st.caption(f"😊 Emotion detected: {message['emotion']}")
                    if message.get("understanding_level"):
                        st.caption(f"📊 Understanding level: {message['understanding_level']}/10")
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = get_ai_response(prompt, session_type)
                
                if response_data:
                    st.write(response_data["response"])
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_data["response"],
                        "emotion": response_data.get("emotion_detected"),
                        "understanding_level": response_data.get("understanding_level"),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Show additional info
                    if response_data.get("emotion_detected"):
                        st.caption(f"😊 Emotion detected: {response_data['emotion_detected']}")
                    if response_data.get("understanding_level"):
                        st.caption(f"📊 Understanding level: {response_data['understanding_level']}/10")
                    
                    # Show suggestions if available
                    if response_data.get("suggestions"):
                        st.subheader("💡 Suggestions for you:")
                        for suggestion in response_data["suggestions"]:
                            st.info(f"• {suggestion}")
                else:
                    error_msg = "I'm having trouble connecting right now. Please try again!"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })

def get_ai_response(message: str, session_type: str = "general") -> Dict[str, Any]:
    """Get AI response from backend API"""
    try:
        # Try to connect to your actual backend
        API_BASE = "http://127.0.0.1:8000"
        
        response = requests.post(
            f"{API_BASE}/api/chat/message",
            params={
                "message": message,
                "session_type": session_type
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback to demo response
            return get_demo_response(message, session_type)
            
    except Exception as e:
        print(f"API Error: {e}")
        # Fallback to demo response
        return get_demo_response(message, session_type)

def get_demo_response(message: str, session_type: str) -> Dict[str, Any]:
    """Fallback demo responses when API is unavailable"""
    import random
    
    responses = [
        {
            "response": f"That's a great question about '{message}'! 😊 Let me help you understand this better. Can you tell me what specific part you'd like to explore?",
            "emotion_detected": "curious",
            "understanding_level": random.randint(6, 8),
            "suggestions": ["Try breaking down the problem into smaller steps", "Review related concepts first"]
        },
        {
            "response": f"I can see you're working on '{message}'. That's awesome! 🎯 How confident do you feel about this topic on a scale of 1-10?",
            "emotion_detected": "encouraging", 
            "understanding_level": random.randint(5, 9),
            "suggestions": ["Practice with similar examples", "Create a summary of key points"]
        }
    ]
    
    if session_type == "study_session":
        responses.append({
            "response": f"Great! Let's focus on '{message}' for this study session. 📚 I'll help you understand this thoroughly. How much time do you have today?",
            "emotion_detected": "focused",
            "understanding_level": random.randint(6, 9),
            "suggestions": ["Set a specific goal for this session", "Take notes while we work"]
        })
    
    return random.choice(responses)


# In the render_quick_actions function, add unique keys to buttons:

def render_quick_actions():
    """Render quick action buttons"""
    st.subheader("🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Start Study Session", key="quick_study_session", use_container_width=True):
            st.info("Starting focused study session...")
            # Add study session logic here
        
        if st.button("🎯 Set Study Goal", key="quick_study_goal", use_container_width=True):
            st.info("Setting new study goal...")
            # Add goal setting logic here
    
    with col2:
        if st.button("📊 Quick Progress Check", key="quick_progress_check", use_container_width=True):
            st.info("Checking your recent progress...")
            # Add progress check logic here
        
        if st.button("💡 Get Study Tip", key="quick_study_tip", use_container_width=True):
            tips = [
                "Take a 5-minute break every 25 minutes of studying",
                "Review your notes within 24 hours of learning",
                "Use active recall instead of just re-reading",
                "Create visual mind maps for complex topics"
            ]
            import random
            st.success(f"💡 Tip: {random.choice(tips)}")


def render_emotion_tracker():
    """Render emotion tracking widget"""
    with st.expander("😊 How are you feeling today?"):
        emotion = st.select_slider(
            "Emotional state:",
            options=["😢 Sad", "😟 Stressed", "😐 Neutral", "😊 Happy", "🎉 Excited"],
            value="😐 Neutral"
        )
        
        if st.button("Log Emotion"):
            st.success(f"Logged: {emotion}")
            # Here you would send this data to your backend

def render_study_timer():
    """Render Pomodoro study timer"""
    with st.expander("⏰ Study Timer"):
        col1, col2 = st.columns(2)
        
        with col1:
            timer_duration = st.selectbox(
                "Timer Duration:",
                [15, 25, 30, 45, 60],
                index=1,
                format_func=lambda x: f"{x} minutes"
            )
        
        with col2:
            if st.button("▶️ Start Timer", use_container_width=True):
                st.success(f"Timer started for {timer_duration} minutes!")
                # Here you would implement actual timer functionality
        
        # Timer display (mock)
        if 'timer_active' in st.session_state and st.session_state.timer_active:
            st.info("🔄 Timer running: 15:32 remaining")

def render_subject_selector():
    """Render quick subject selection for focused study"""
    with st.expander("📚 Quick Subject Focus"):
        subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Literature", "History"]
        
        selected_subject = st.selectbox("Choose subject for focused help:", subjects)
        
        if st.button("💡 Get Subject Tips"):
            tips = {
                "Mathematics": "Try visualizing problems with diagrams and practice step-by-step solutions",
                "Physics": "Connect concepts to real-world examples and practice problem-solving methods",
                "Chemistry": "Use molecular models and practice balancing equations regularly",
                "Biology": "Create concept maps and use flashcards for terminology",
                "Literature": "Read actively, take notes, and analyze themes and characters",
                "History": "Create timelines and connect events to understand cause and effect"
            }
            
            st.info(f"💡 **{selected_subject} Tips**: {tips.get(selected_subject, 'Keep practicing and stay curious!')}")

def render_conversation_export():
    """Render conversation export functionality"""
    if st.session_state.messages:
        with st.expander("💾 Export Conversation"):
            if st.button("📥 Download Chat History"):
                # Convert messages to text format
                chat_text = ""
                for msg in st.session_state.messages:
                    role = "You" if msg["role"] == "user" else "AI Tutor"
                    chat_text += f"{role}: {msg['content']}\n\n"
                
                st.download_button(
                    label="📄 Download as Text File",
                    data=chat_text,
                    file_name=f"ai_tutor_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
