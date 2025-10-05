# Analytics dashboard
"""
Dashboard component for displaying student analytics and progress
Shows charts, statistics, and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def render_dashboard():
    """Render the main dashboard with analytics"""
    st.title("📊 Your Learning Dashboard")
    
    # Overview metrics
    render_overview_metrics()
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        render_study_progress_chart()
        render_subject_distribution()
    
    with col2:
        render_understanding_trends()
        render_emotion_trends()
    
    # Recent activity
    render_recent_activity()
    
    # Study insights
    render_study_insights()
    
    # Goals tracker
    render_goal_tracker()

def render_overview_metrics():
    """Render overview metrics cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate mock data - replace with actual API calls
    study_streak = random.randint(3, 15)
    total_hours = random.randint(20, 80)
    active_subjects = random.randint(2, 6)
    avg_understanding = round(random.uniform(6.5, 9.2), 1)
    
    with col1:
        st.metric(
            label="📅 Study Streak",
            value=f"{study_streak} days",
            delta=f"+{random.randint(1, 3)} days"
        )
    
    with col2:
        st.metric(
            label="⏰ Total Study Time",
            value=f"{total_hours}h",
            delta=f"+{random.randint(2, 8)}h this week"
        )
    
    with col3:
        st.metric(
            label="📚 Active Subjects", 
            value=active_subjects,
            delta=f"+{random.randint(0, 2)}"
        )
    
    with col4:
        st.metric(
            label="🎯 Avg Understanding",
            value=f"{avg_understanding}/10",
            delta=f"+{random.uniform(0.1, 0.8):.1f}"
        )

def render_study_progress_chart():
    """Render weekly study progress chart"""
    st.subheader("📈 Weekly Study Progress")
    
    # Mock data - replace with actual data from API
    dates = pd.date_range(start=datetime.now() - timedelta(days=6), end=datetime.now(), freq='D')
    study_minutes = [random.randint(30, 180) for _ in range(7)]
    
    df = pd.DataFrame({
        'Date': dates,
        'Study Time (mins)': study_minutes
    })
    
    fig = px.bar(
        df, 
        x='Date', 
        y='Study Time (mins)',
        title="Daily Study Time",
        color='Study Time (mins)',
        color_continuous_scale='Blues'
    )
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

def render_understanding_trends():
    """Render understanding level trends by subject"""
    st.subheader("🎯 Understanding Trends")
    
    # Mock data
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Literature', 'History']
    understanding_levels = [random.uniform(6.0, 9.5) for _ in subjects]
    
    df = pd.DataFrame({
        'Subject': subjects,
        'Understanding Level': understanding_levels
    })
    
    fig = px.bar(
        df,
        x='Subject', 
        y='Understanding Level',
        color='Understanding Level',
        color_continuous_scale='RdYlGn',
        title="Current Understanding by Subject"
    )
    fig.update_layout(showlegend=False, height=300)
    fig.update_yaxis(range=[0, 10])
    st.plotly_chart(fig, use_container_width=True)

def render_subject_distribution():
    """Render pie chart of time spent by subject"""
    st.subheader("🥧 Time Distribution by Subject")
    
    # Mock data
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Literature']
    time_spent = [random.randint(300, 800) for _ in subjects]
    
    fig = px.pie(
        values=time_spent,
        names=subjects,
        title="Study Time Distribution (minutes)"
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def render_emotion_trends():
    """Render emotional state trends over time"""
    st.subheader("😊 Emotional Wellbeing")
    
    # Mock data
    dates = pd.date_range(start=datetime.now() - timedelta(days=13), end=datetime.now(), freq='D')
    emotions = ['happy', 'neutral', 'stressed', 'excited', 'confused']
    emotion_scores = {
        'happy': 4,
        'excited': 5,
        'neutral': 3,
        'confused': 2, 
        'stressed': 1
    }
    
    daily_emotions = [random.choice(emotions) for _ in dates]
    daily_scores = [emotion_scores[emotion] for emotion in daily_emotions]
    
    df = pd.DataFrame({
        'Date': dates,
        'Emotion Score': daily_scores,
        'Emotion': daily_emotions
    })
    
    fig = px.line(
        df,
        x='Date',
        y='Emotion Score',
        title="Emotional Wellbeing Trend",
        markers=True
    )
    fig.update_layout(height=300)
    fig.update_yaxis(range=[0, 6])
    st.plotly_chart(fig, use_container_width=True)

def render_recent_activity():
    """Render recent study activity table"""
    st.subheader("📚 Recent Study Sessions")
    
    # Mock data
    sessions_data = []
    for i in range(5):
        sessions_data.append({
            'Date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            'Subject': random.choice(['Mathematics', 'Physics', 'Chemistry', 'Literature']),
            'Topic': random.choice([
                'Calculus Integration', 'Quantum Mechanics', 'Organic Chemistry',
                'Shakespeare Analysis', 'Linear Algebra', 'Thermodynamics'
            ]),
            'Duration': f"{random.randint(30, 120)} min",
            'Understanding': f"{random.randint(6, 10)}/10",
            'Status': random.choice(['✅ Completed', '📚 In Progress', '⭐ Mastered'])
        })
    
    df = pd.DataFrame(sessions_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_study_insights():
    """Render AI-generated study insights"""
    st.subheader("🧠 AI Insights & Recommendations")
    
    # Mock insights - replace with actual AI-generated insights
    insights = [
        "🎯 **Great Progress!** Your understanding in Mathematics has improved by 15% this week.",
        "📚 **Study Pattern:** You're most productive during morning sessions (9-11 AM).",
        "⚡ **Quick Win:** Spend 15 more minutes on Chemistry to reach your weekly goal.",
        "🌟 **Strength:** You're excelling in Physics - consider helping peers or taking advanced topics.",
        "🔄 **Suggestion:** Take a 5-minute break every 25 minutes to improve focus (Pomodoro technique)."
    ]
    
    for insight in insights:
        st.info(insight)

def render_goal_tracker():
    """Render goal tracking section"""
    st.subheader("🎯 Weekly Goals")
    
    goals = [
        {"goal": "Study Mathematics 5 hours", "progress": 80, "target": 300, "current": 240},
        {"goal": "Complete Chemistry assignments", "progress": 60, "target": 5, "current": 3},
        {"goal": "Read 2 literature chapters", "progress": 100, "target": 2, "current": 2},
        {"goal": "Physics problem solving", "progress": 45, "target": 20, "current": 9}
    ]
    
    for goal in goals:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(goal["goal"])
            progress_bar = st.progress(goal["progress"] / 100)
        
        with col2:
            if goal["progress"] >= 100:
                st.success("✅ Done")
            else:
                st.write(f"{goal['progress']}%")
        
        with col3:
            st.caption(f"{goal['current']}/{goal['target']}")

def render_achievements():
    """Render achievements and badges"""
    st.subheader("🏆 Achievements")
    
    achievements = [
        {"title": "🔥 Study Streak Master", "desc": "7 consecutive days", "earned": True},
        {"title": "📚 Knowledge Seeker", "desc": "50 topics studied", "earned": True},
        {"title": "🎯 Perfect Score", "desc": "10/10 understanding", "earned": False},
        {"title": "⏰ Time Keeper", "desc": "100 hours studied", "earned": False},
    ]
    
    cols = st.columns(2)
    
    for i, achievement in enumerate(achievements):
        with cols[i % 2]:
            if achievement["earned"]:
                st.success(f"**{achievement['title']}**\n{achievement['desc']}")
            else:
                st.info(f"**{achievement['title']}**\n{achievement['desc']} (Not earned)")

def render_weekly_summary():
    """Render weekly performance summary"""
    with st.expander("📋 Weekly Summary", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**This Week's Highlights:**")
            st.markdown("• Completed 12 study sessions")
            st.markdown("• Improved in 3 subjects")
            st.markdown("• Maintained daily study habit")
            st.markdown("• Asked 15 thoughtful questions")
        
        with col2:
            st.markdown("**Areas for Improvement:**")
            st.markdown("• Increase Chemistry study time")
            st.markdown("• Review Literature concepts")
            st.markdown("• Practice more Math problems")
            st.markdown("• Take regular breaks")

def render_comparison_chart():
    """Render performance comparison with previous periods"""
    st.subheader("📈 Performance Comparison")
    
    periods = ['2 weeks ago', 'Last week', 'This week']
    study_time = [15, 18, 22]
    understanding = [7.2, 7.8, 8.3]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Study Time (hours)',
        x=periods,
        y=study_time,
        yaxis='y',
        offsetgroup=1
    ))
    
    fig.add_trace(go.Scatter(
        name='Avg Understanding',
        x=periods,
        y=understanding,
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='orange', width=3)
    ))
    
    fig.update_layout(
        title="Study Time vs Understanding Level",
        yaxis=dict(title="Study Time (hours)"),
        yaxis2=dict(title="Understanding Level", overlaying='y', side='right', range=[0, 10]),
        legend=dict(x=0.7, y=1),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
